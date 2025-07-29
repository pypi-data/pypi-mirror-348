from __future__ import annotations

import contextlib
import logging
from asyncio import CancelledError
from contextlib import contextmanager
from threading import Thread
from typing import TYPE_CHECKING, Any, Callable, cast

import psycopg
import psycopg.errors
import psycopg_pool
from psycopg import Connection, Cursor, Error
from psycopg.generators import notifies
from psycopg.rows import DictRow, dict_row
from psycopg.sql import SQL, Composed, Identifier
from typing_extensions import TypeVar

from eventsourcing.persistence import (
    AggregateRecorder,
    ApplicationRecorder,
    DatabaseError,
    DataError,
    InfrastructureFactory,
    IntegrityError,
    InterfaceError,
    InternalError,
    ListenNotifySubscription,
    Notification,
    NotSupportedError,
    OperationalError,
    PersistenceError,
    ProcessRecorder,
    ProgrammingError,
    StoredEvent,
    Subscription,
    Tracking,
    TrackingRecorder,
)
from eventsourcing.utils import Environment, EnvType, resolve_topic, retry, strtobool

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from uuid import UUID

    from psycopg.abc import Query
    from typing_extensions import Self

logging.getLogger("psycopg.pool").setLevel(logging.ERROR)
logging.getLogger("psycopg").setLevel(logging.ERROR)

# Copy of "private" psycopg.errors._NO_TRACEBACK (in case it changes)
# From psycopg: "Don't show a complete traceback upon raising these exception.
# Usually the traceback starts from internal functions (for instance in the
# server communication callbacks) but, for the end user, it's more important
# to get the high level information about where the exception was raised, for
# instance in a certain `Cursor.execute()`."
NO_TRACEBACK = (Error, KeyboardInterrupt, CancelledError)


class ConnectionPool(psycopg_pool.ConnectionPool[Any]):
    def __init__(
        self,
        *args: Any,
        get_password_func: Callable[[], str] | None = None,
        **kwargs: Any,
    ) -> None:
        self.get_password_func = get_password_func
        super().__init__(*args, **kwargs)

    def _connect(self, timeout: float | None = None) -> Connection[Any]:
        if self.get_password_func:
            self.kwargs["password"] = self.get_password_func()
        return super()._connect(timeout=timeout)


class PostgresDatastore:
    def __init__(  # noqa: PLR0913
        self,
        dbname: str,
        host: str,
        port: str | int,
        user: str,
        password: str,
        *,
        connect_timeout: float = 5.0,
        idle_in_transaction_session_timeout: float = 0,
        pool_size: int = 1,
        max_overflow: int = 0,
        max_waiting: int = 0,
        conn_max_age: float = 60 * 60.0,
        pre_ping: bool = False,
        lock_timeout: int = 0,
        schema: str = "",
        pool_open_timeout: float | None = None,
        get_password_func: Callable[[], str] | None = None,
        single_row_tracking: bool = True,
    ):
        self.idle_in_transaction_session_timeout = idle_in_transaction_session_timeout
        self.pre_ping = pre_ping
        self.pool_open_timeout = pool_open_timeout
        self.single_row_tracking = single_row_tracking

        check = ConnectionPool.check_connection if pre_ping else None
        self.pool = ConnectionPool(
            get_password_func=get_password_func,
            connection_class=Connection[DictRow],
            kwargs={
                "dbname": dbname,
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "row_factory": dict_row,
            },
            min_size=pool_size,
            max_size=pool_size + max_overflow,
            open=False,
            configure=self.after_connect_func(),
            timeout=connect_timeout,
            max_waiting=max_waiting,
            max_lifetime=conn_max_age,
            check=check,
        )
        self.lock_timeout = lock_timeout
        self.schema = schema.strip() or "public"

    def after_connect_func(self) -> Callable[[Connection[Any]], None]:
        statement = SQL("SET idle_in_transaction_session_timeout = '{0}ms'").format(
            int(self.idle_in_transaction_session_timeout * 1000)
        )

        def after_connect(conn: Connection[DictRow]) -> None:
            conn.autocommit = True
            conn.cursor().execute(statement)

        return after_connect

    @contextmanager
    def get_connection(self) -> Iterator[Connection[DictRow]]:
        try:
            wait = self.pool_open_timeout is not None
            timeout = self.pool_open_timeout or 30.0
            self.pool.open(wait, timeout)

            with self.pool.connection() as conn:
                yield conn
        except psycopg.InterfaceError as e:
            # conn.close()
            raise InterfaceError(str(e)) from e
        except psycopg.OperationalError as e:
            # conn.close()
            raise OperationalError(str(e)) from e
        except psycopg.DataError as e:
            raise DataError(str(e)) from e
        except psycopg.IntegrityError as e:
            raise IntegrityError(str(e)) from e
        except psycopg.InternalError as e:
            raise InternalError(str(e)) from e
        except psycopg.ProgrammingError as e:
            raise ProgrammingError(str(e)) from e
        except psycopg.NotSupportedError as e:
            raise NotSupportedError(str(e)) from e
        except psycopg.DatabaseError as e:
            raise DatabaseError(str(e)) from e
        except psycopg.Error as e:
            # conn.close()
            raise PersistenceError(str(e)) from e
        except Exception:
            # conn.close()
            raise

    @contextmanager
    def transaction(self, *, commit: bool = False) -> Iterator[Cursor[DictRow]]:
        with self.get_connection() as conn, conn.transaction(force_rollback=not commit):
            yield conn.cursor()

    def close(self) -> None:
        self.pool.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object, **kwargs: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()


class PostgresRecorder:
    """Base class for recorders that use PostgreSQL."""

    MAX_IDENTIFIER_LEN = 63
    # From the PostgreSQL docs: "The system uses no more than NAMEDATALEN-1 bytes
    # of an identifier; longer names can be written in commands, but they will be
    # truncated. By default, NAMEDATALEN is 64 so the maximum identifier length is
    # 63 bytes." https://www.postgresql.org/docs/current/sql-syntax-lexical.html

    def __init__(
        self,
        datastore: PostgresDatastore,
    ):
        self.datastore = datastore
        self.create_table_statements = self.construct_create_table_statements()

    @staticmethod
    def check_table_name_length(table_name: str) -> None:
        if len(table_name) > PostgresRecorder.MAX_IDENTIFIER_LEN:
            msg = f"Table name too long: {table_name}"
            raise ProgrammingError(msg)

    def construct_create_table_statements(self) -> list[Composed]:
        return []

    def create_table(self) -> None:
        with self.datastore.transaction(commit=True) as curs:
            self._create_table(curs)

    def _create_table(self, curs: Cursor[DictRow]) -> None:
        for statement in self.create_table_statements:
            curs.execute(statement, prepare=False)


class PostgresAggregateRecorder(PostgresRecorder, AggregateRecorder):
    def __init__(
        self,
        datastore: PostgresDatastore,
        *,
        events_table_name: str = "stored_events",
    ):
        super().__init__(datastore)
        self.check_table_name_length(events_table_name)
        self.events_table_name = events_table_name
        # Index names can't be qualified names, but
        # are created in the same schema as the table.
        self.notification_id_index_name = (
            f"{self.events_table_name}_notification_id_idx"
        )
        self.create_table_statements.append(
            SQL(
                "CREATE TABLE IF NOT EXISTS {0}.{1} ("
                "originator_id uuid NOT NULL, "
                "originator_version bigint NOT NULL, "
                "topic text, "
                "state bytea, "
                "PRIMARY KEY "
                "(originator_id, originator_version)) "
                "WITH (autovacuum_enabled=false)"
            ).format(
                Identifier(self.datastore.schema),
                Identifier(self.events_table_name),
            )
        )

        self.insert_events_statement = SQL(
            "INSERT INTO {0}.{1} VALUES (%s, %s, %s, %s)"
        ).format(
            Identifier(self.datastore.schema),
            Identifier(self.events_table_name),
        )

        self.select_events_statement = SQL(
            "SELECT * FROM {0}.{1} WHERE originator_id = %s"
        ).format(
            Identifier(self.datastore.schema),
            Identifier(self.events_table_name),
        )

        self.lock_table_statements: list[Query] = []

    @retry((InterfaceError, OperationalError), max_attempts=10, wait=0.2)
    def insert_events(
        self, stored_events: Sequence[StoredEvent], **kwargs: Any
    ) -> Sequence[int] | None:
        exc: Exception | None = None
        notification_ids: Sequence[int] | None = None
        with self.datastore.get_connection() as conn:
            with conn.pipeline() as pipeline, conn.transaction():
                # Do other things first, so they can be pipelined too.
                with conn.cursor() as curs:
                    self._insert_events(curs, stored_events, **kwargs)
                # Then use a different cursor for the executemany() call.
                with conn.cursor() as curs:
                    try:
                        self._insert_stored_events(curs, stored_events, **kwargs)
                        # Sync now, so any uniqueness constraint violation causes an
                        # IntegrityError to be raised here, rather an InternalError
                        # being raised sometime later e.g. when commit() is called.
                        pipeline.sync()
                        notification_ids = self._fetch_ids_after_insert_events(
                            curs, stored_events, **kwargs
                        )
                    except Exception as e:
                        # Avoid psycopg emitting a pipeline warning.
                        exc = e
            if exc:
                # Reraise exception after pipeline context manager has exited.
                raise exc
        return notification_ids

    def _insert_events(
        self,
        curs: Cursor[DictRow],
        stored_events: Sequence[StoredEvent],
        **_: Any,
    ) -> None:
        pass

    def _insert_stored_events(
        self,
        curs: Cursor[DictRow],
        stored_events: Sequence[StoredEvent],
        **_: Any,
    ) -> None:
        # Only do something if there is something to do.
        if len(stored_events) > 0:
            self._lock_table(curs)

            self._notify_channel(curs)

            # Insert events.
            curs.executemany(
                query=self.insert_events_statement,
                params_seq=[
                    (
                        stored_event.originator_id,
                        stored_event.originator_version,
                        stored_event.topic,
                        stored_event.state,
                    )
                    for stored_event in stored_events
                ],
                returning="RETURNING" in self.insert_events_statement.as_string(),
            )

    def _lock_table(self, curs: Cursor[DictRow]) -> None:
        pass

    def _notify_channel(self, curs: Cursor[DictRow]) -> None:
        pass

    def _fetch_ids_after_insert_events(
        self,
        curs: Cursor[DictRow],
        stored_events: Sequence[StoredEvent],
        **kwargs: Any,
    ) -> Sequence[int] | None:
        return None

    @retry((InterfaceError, OperationalError), max_attempts=10, wait=0.2)
    def select_events(
        self,
        originator_id: UUID | str,
        *,
        gt: int | None = None,
        lte: int | None = None,
        desc: bool = False,
        limit: int | None = None,
    ) -> Sequence[StoredEvent]:
        statement = self.select_events_statement
        params: list[Any] = [originator_id]
        if gt is not None:
            params.append(gt)
            statement += SQL(" AND originator_version > %s")
        if lte is not None:
            params.append(lte)
            statement += SQL(" AND originator_version <= %s")
        statement += SQL(" ORDER BY originator_version")
        if desc is False:
            statement += SQL(" ASC")
        else:
            statement += SQL(" DESC")
        if limit is not None:
            params.append(limit)
            statement += SQL(" LIMIT %s")

        with self.datastore.get_connection() as conn, conn.cursor() as curs:
            curs.execute(statement, params, prepare=True)
            return [
                StoredEvent(
                    originator_id=row["originator_id"],
                    originator_version=row["originator_version"],
                    topic=row["topic"],
                    state=bytes(row["state"]),
                )
                for row in curs.fetchall()
            ]


class PostgresApplicationRecorder(PostgresAggregateRecorder, ApplicationRecorder):
    def __init__(
        self,
        datastore: PostgresDatastore,
        *,
        events_table_name: str = "stored_events",
    ):
        super().__init__(datastore, events_table_name=events_table_name)
        self.create_table_statements[-1] = SQL(
            "CREATE TABLE IF NOT EXISTS {0}.{1} ("
            "originator_id uuid NOT NULL, "
            "originator_version bigint NOT NULL, "
            "topic text, "
            "state bytea, "
            "notification_id bigserial, "
            "PRIMARY KEY "
            "(originator_id, originator_version)) "
            "WITH (autovacuum_enabled=false)"
        ).format(
            Identifier(self.datastore.schema),
            Identifier(self.events_table_name),
        )

        self.create_table_statements.append(
            SQL(
                "CREATE UNIQUE INDEX IF NOT EXISTS {0} "
                "ON {1}.{2} (notification_id ASC);"
            ).format(
                Identifier(self.notification_id_index_name),
                Identifier(self.datastore.schema),
                Identifier(self.events_table_name),
            )
        )

        self.channel_name = self.events_table_name.replace(".", "_")
        self.insert_events_statement = self.insert_events_statement + SQL(
            " RETURNING notification_id"
        )

        self.max_notification_id_statement = SQL(
            "SELECT MAX(notification_id) FROM {0}.{1}"
        ).format(
            Identifier(self.datastore.schema),
            Identifier(self.events_table_name),
        )

        self.lock_table_statements = [
            SQL("SET LOCAL lock_timeout = '{0}s'").format(self.datastore.lock_timeout),
            SQL("LOCK TABLE {0}.{1} IN EXCLUSIVE MODE").format(
                Identifier(self.datastore.schema),
                Identifier(self.events_table_name),
            ),
        ]

    @retry((InterfaceError, OperationalError), max_attempts=10, wait=0.2)
    def select_notifications(
        self,
        start: int | None,
        limit: int,
        stop: int | None = None,
        topics: Sequence[str] = (),
        *,
        inclusive_of_start: bool = True,
    ) -> Sequence[Notification]:
        """Returns a list of event notifications
        from 'start', limited by 'limit'.
        """
        params: list[int | str | Sequence[str]] = []
        statement = SQL("SELECT * FROM {0}.{1}").format(
            Identifier(self.datastore.schema),
            Identifier(self.events_table_name),
        )
        has_where = False
        if start is not None:
            statement += SQL(" WHERE")
            has_where = True
            params.append(start)
            if inclusive_of_start:
                statement += SQL(" notification_id>=%s")
            else:
                statement += SQL(" notification_id>%s")

        if stop is not None:
            if not has_where:
                has_where = True
                statement += SQL(" WHERE")
            else:
                statement += SQL(" AND")

            params.append(stop)
            statement += SQL(" notification_id <= %s")

        if topics:
            # Check sequence and ensure list of strings.
            assert isinstance(topics, (tuple, list)), topics
            topics = list(topics) if isinstance(topics, tuple) else topics
            assert all(isinstance(t, str) for t in topics), topics
            if not has_where:
                statement += SQL(" WHERE")
            else:
                statement += SQL(" AND")
            params.append(topics)
            statement += SQL(" topic = ANY(%s)")

        params.append(limit)
        statement += SQL(" ORDER BY notification_id LIMIT %s")

        connection = self.datastore.get_connection()
        with connection as conn, conn.cursor() as curs:
            curs.execute(statement, params, prepare=True)
            return [
                Notification(
                    id=row["notification_id"],
                    originator_id=row["originator_id"],
                    originator_version=row["originator_version"],
                    topic=row["topic"],
                    state=bytes(row["state"]),
                )
                for row in curs.fetchall()
            ]

    @retry((InterfaceError, OperationalError), max_attempts=10, wait=0.2)
    def max_notification_id(self) -> int | None:
        """Returns the maximum notification ID."""
        with self.datastore.get_connection() as conn, conn.cursor() as curs:
            curs.execute(self.max_notification_id_statement)
            fetchone = curs.fetchone()
            assert fetchone is not None
            return fetchone["max"]

    def _lock_table(self, curs: Cursor[DictRow]) -> None:
        # Acquire "EXCLUSIVE" table lock, to serialize transactions that insert
        # stored events, so that readers don't pass over gaps that are filled in
        # later. We want each transaction that will be issued with notifications
        # IDs by the notification ID sequence to receive all its notification IDs
        # and then commit, before another transaction is issued with any notification
        # IDs. In other words, we want the insert order to be the same as the commit
        # order. We can accomplish this by locking the table for writes. The
        # EXCLUSIVE lock mode does not block SELECT statements, which acquire an
        # ACCESS SHARE lock, so the stored events table can be read concurrently
        # with writes and other reads. However, INSERT statements normally just
        # acquires ROW EXCLUSIVE locks, which risks the interleaving (within the
        # recorded sequence of notification IDs) of stored events from one transaction
        # with those of another transaction. And since one transaction will always
        # commit before another, the possibility arises when using ROW EXCLUSIVE locks
        # for readers that are tailing a notification log to miss items inserted later
        # but issued with lower notification IDs.
        # https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-TABLES
        # https://www.postgresql.org/docs/9.1/sql-lock.html
        # https://stackoverflow.com/questions/45866187/guarantee-monotonicity-of
        # -postgresql-serial-column-values-by-commit-order
        for lock_statement in self.lock_table_statements:
            curs.execute(lock_statement, prepare=True)

    def _notify_channel(self, curs: Cursor[DictRow]) -> None:
        curs.execute(SQL("NOTIFY {0}").format(Identifier(self.channel_name)))

    def _fetch_ids_after_insert_events(
        self,
        curs: Cursor[DictRow],
        stored_events: Sequence[StoredEvent],
        **kwargs: Any,
    ) -> Sequence[int] | None:
        notification_ids: list[int] = []
        len_events = len(stored_events)
        if len_events:
            while curs.nextset() and len(notification_ids) != len_events:
                if curs.statusmessage and curs.statusmessage.startswith("INSERT"):
                    row = curs.fetchone()
                    assert row is not None
                    notification_ids.append(row["notification_id"])
            if len(notification_ids) != len(stored_events):
                msg = "Couldn't get all notification IDs "
                msg += f"(got {len(notification_ids)}, expected {len(stored_events)})"
                raise ProgrammingError(msg)
        return notification_ids

    def subscribe(
        self, gt: int | None = None, topics: Sequence[str] = ()
    ) -> Subscription[ApplicationRecorder]:
        return PostgresSubscription(recorder=self, gt=gt, topics=topics)


class PostgresSubscription(ListenNotifySubscription[PostgresApplicationRecorder]):
    def __init__(
        self,
        recorder: PostgresApplicationRecorder,
        gt: int | None = None,
        topics: Sequence[str] = (),
    ) -> None:
        assert isinstance(recorder, PostgresApplicationRecorder)
        super().__init__(recorder=recorder, gt=gt, topics=topics)
        self._listen_thread = Thread(target=self._listen)
        self._listen_thread.start()

    def __exit__(self, *args: object, **kwargs: Any) -> None:
        super().__exit__(*args, **kwargs)
        self._listen_thread.join()

    def _listen(self) -> None:
        try:
            with self._recorder.datastore.get_connection() as conn:
                conn.execute(
                    SQL("LISTEN {0}").format(Identifier(self._recorder.channel_name))
                )
                while not self._has_been_stopped and not self._thread_error:
                    # This block simplifies psycopg's conn.notifies(), because
                    # we aren't interested in the actual notify messages, and
                    # also we want to stop consuming notify messages when the
                    # subscription has an error or is otherwise stopped.
                    with conn.lock:
                        try:
                            if conn.wait(notifies(conn.pgconn), interval=0.1):
                                self._has_been_notified.set()
                        except NO_TRACEBACK as ex:  # pragma: no cover
                            raise ex.with_traceback(None) from None

        except BaseException as e:
            if self._thread_error is None:
                self._thread_error = e
            self.stop()


class PostgresTrackingRecorder(PostgresRecorder, TrackingRecorder):
    def __init__(
        self,
        datastore: PostgresDatastore,
        *,
        tracking_table_name: str = "notification_tracking",
        **kwargs: Any,
    ):
        super().__init__(datastore, **kwargs)
        self.check_table_name_length(tracking_table_name)
        self.tracking_table_name = tracking_table_name
        self.tracking_table_exists: bool = False
        self.tracking_migration_previous: int | None = None
        self.tracking_migration_current: int | None = None
        self.table_migration_identifier = "__migration__"
        self.has_checked_for_multi_row_tracking_table: bool = False
        if self.datastore.single_row_tracking:
            # For single-row tracking.
            self.create_table_statements.append(
                SQL(
                    "CREATE TABLE IF NOT EXISTS {0}.{1} ("
                    "application_name text, "
                    "notification_id bigint, "
                    "PRIMARY KEY "
                    "(application_name))"
                ).format(
                    Identifier(self.datastore.schema),
                    Identifier(self.tracking_table_name),
                )
            )
            self.insert_tracking_statement = SQL(
                "INSERT INTO {0}.{1} "
                "VALUES (%(application_name)s, %(notification_id)s) "
                "ON CONFLICT (application_name) DO UPDATE "
                "SET notification_id = %(notification_id)s "
                "WHERE {0}.{1}.notification_id < %(notification_id)s "
                "RETURNING notification_id"
            ).format(
                Identifier(self.datastore.schema),
                Identifier(self.tracking_table_name),
            )
        else:
            # For legacy multi-row tracking.
            self.create_table_statements.append(
                SQL(
                    "CREATE TABLE IF NOT EXISTS {0}.{1} ("
                    "application_name text, "
                    "notification_id bigint, "
                    "PRIMARY KEY "
                    "(application_name, notification_id))"
                ).format(
                    Identifier(self.datastore.schema),
                    Identifier(self.tracking_table_name),
                )
            )
            self.insert_tracking_statement = SQL(
                "INSERT INTO {0}.{1} VALUES (%(application_name)s, %(notification_id)s)"
            ).format(
                Identifier(self.datastore.schema),
                Identifier(self.tracking_table_name),
            )

        self.max_tracking_id_statement = SQL(
            "SELECT MAX(notification_id) FROM {0}.{1} WHERE application_name=%s"
        ).format(
            Identifier(self.datastore.schema),
            Identifier(self.tracking_table_name),
        )

    def create_table(self) -> None:
        # Get the migration version.
        try:
            self.tracking_migration_current = self.tracking_migration_previous = (
                self.max_tracking_id(self.table_migration_identifier)
            )
        except ProgrammingError:
            pass
        else:
            self.tracking_table_exists = True
        super().create_table()
        if (
            not self.datastore.single_row_tracking
            and self.tracking_migration_current is not None
        ):
            msg = "Can't do multi-row tracking with single-row tracking table"
            raise OperationalError(msg)

    def _create_table(self, curs: Cursor[DictRow]) -> None:
        max_tracking_ids: dict[str, int] = {}
        if (
            self.datastore.single_row_tracking
            and self.tracking_table_exists
            and not self.tracking_migration_previous
        ):
            # Migrate the table.
            curs.execute(
                SQL("SET LOCAL lock_timeout = '{0}s'").format(
                    self.datastore.lock_timeout
                )
            )
            curs.execute(
                SQL("LOCK TABLE {0}.{1} IN ACCESS EXCLUSIVE MODE").format(
                    Identifier(self.datastore.schema),
                    Identifier(self.tracking_table_name),
                )
            )

            # Get all application names.
            application_names: list[str] = [
                select_row["application_name"]
                for select_row in curs.execute(
                    SQL("SELECT DISTINCT application_name FROM {0}.{1}").format(
                        Identifier(self.datastore.schema),
                        Identifier(self.tracking_table_name),
                    )
                )
            ]

            # Get max tracking ID for each application name.
            for application_name in application_names:
                curs.execute(self.max_tracking_id_statement, (application_name,))
                max_tracking_id_row = curs.fetchone()
                assert max_tracking_id_row is not None
                max_tracking_ids[application_name] = max_tracking_id_row["max"]
            # Rename the table.
            rename = f"bkup1_{self.tracking_table_name}"[: self.MAX_IDENTIFIER_LEN]
            drop_table_statement = SQL("ALTER TABLE {0}.{1} RENAME TO {2}").format(
                Identifier(self.datastore.schema),
                Identifier(self.tracking_table_name),
                Identifier(rename),
            )
            curs.execute(drop_table_statement)
        # Create the table.
        super()._create_table(curs)
        # Maybe insert migration tracking record and application tracking records.
        if self.datastore.single_row_tracking and (
            not self.tracking_table_exists
            or (self.tracking_table_exists and not self.tracking_migration_previous)
        ):
            # Assume we just created a table for single-row tracking.
            self._insert_tracking(curs, Tracking(self.table_migration_identifier, 1))
            self.tracking_migration_current = 1
            for application_name, max_tracking_id in max_tracking_ids.items():
                self._insert_tracking(curs, Tracking(application_name, max_tracking_id))

    @retry((InterfaceError, OperationalError), max_attempts=10, wait=0.2)
    def insert_tracking(self, tracking: Tracking) -> None:
        with self.datastore.transaction(commit=True) as curs:
            self._insert_tracking(curs, tracking)

    def _insert_tracking(
        self,
        curs: Cursor[DictRow],
        tracking: Tracking,
    ) -> None:
        self._check_has_multi_row_tracking_table(curs)

        curs.execute(
            query=self.insert_tracking_statement,
            params={
                "application_name": tracking.application_name,
                "notification_id": tracking.notification_id,
            },
            prepare=True,
        )
        if self.datastore.single_row_tracking:
            fetchone = curs.fetchone()
            if fetchone is None:
                msg = (
                    "Failed to record tracking for "
                    f"{tracking.application_name} {tracking.notification_id}"
                )
                raise IntegrityError(msg)

    def _check_has_multi_row_tracking_table(self, c: Cursor[DictRow]) -> None:
        if (
            not self.datastore.single_row_tracking
            and not self.has_checked_for_multi_row_tracking_table
            and self._max_tracking_id(self.table_migration_identifier, c)
        ):
            msg = "Can't do multi-row tracking with single-row tracking table"
            raise ProgrammingError(msg)
        self.has_checked_for_multi_row_tracking_table = True

    @retry((InterfaceError, OperationalError), max_attempts=10, wait=0.2)
    def max_tracking_id(self, application_name: str) -> int | None:
        with self.datastore.get_connection() as conn, conn.cursor() as curs:
            return self._max_tracking_id(application_name, curs)

    def _max_tracking_id(
        self, application_name: str, curs: Cursor[DictRow]
    ) -> int | None:
        curs.execute(
            query=self.max_tracking_id_statement,
            params=(application_name,),
            prepare=True,
        )
        fetchone = curs.fetchone()
        assert fetchone is not None
        return fetchone["max"]

    @retry((InterfaceError, OperationalError), max_attempts=10, wait=0.2)
    def has_tracking_id(
        self, application_name: str, notification_id: int | None
    ) -> bool:
        return super().has_tracking_id(application_name, notification_id)


TPostgresTrackingRecorder = TypeVar(
    "TPostgresTrackingRecorder",
    bound=PostgresTrackingRecorder,
    default=PostgresTrackingRecorder,
)


class PostgresProcessRecorder(
    PostgresTrackingRecorder, PostgresApplicationRecorder, ProcessRecorder
):
    def __init__(
        self,
        datastore: PostgresDatastore,
        *,
        events_table_name: str = "stored_events",
        tracking_table_name: str = "notification_tracking",
    ):
        super().__init__(
            datastore,
            tracking_table_name=tracking_table_name,
            events_table_name=events_table_name,
        )

    def _insert_events(
        self,
        curs: Cursor[DictRow],
        stored_events: Sequence[StoredEvent],
        **kwargs: Any,
    ) -> None:
        tracking: Tracking | None = kwargs.get("tracking")
        if tracking is not None:
            self._insert_tracking(curs, tracking=tracking)
        super()._insert_events(curs, stored_events, **kwargs)


class PostgresFactory(InfrastructureFactory[PostgresTrackingRecorder]):
    POSTGRES_DBNAME = "POSTGRES_DBNAME"
    POSTGRES_HOST = "POSTGRES_HOST"
    POSTGRES_PORT = "POSTGRES_PORT"
    POSTGRES_USER = "POSTGRES_USER"
    POSTGRES_PASSWORD = "POSTGRES_PASSWORD"  # noqa: S105
    POSTGRES_GET_PASSWORD_TOPIC = "POSTGRES_GET_PASSWORD_TOPIC"  # noqa: S105
    POSTGRES_CONNECT_TIMEOUT = "POSTGRES_CONNECT_TIMEOUT"
    POSTGRES_CONN_MAX_AGE = "POSTGRES_CONN_MAX_AGE"
    POSTGRES_PRE_PING = "POSTGRES_PRE_PING"
    POSTGRES_MAX_WAITING = "POSTGRES_MAX_WAITING"
    POSTGRES_LOCK_TIMEOUT = "POSTGRES_LOCK_TIMEOUT"
    POSTGRES_POOL_SIZE = "POSTGRES_POOL_SIZE"
    POSTGRES_MAX_OVERFLOW = "POSTGRES_MAX_OVERFLOW"
    POSTGRES_IDLE_IN_TRANSACTION_SESSION_TIMEOUT = (
        "POSTGRES_IDLE_IN_TRANSACTION_SESSION_TIMEOUT"
    )
    POSTGRES_SCHEMA = "POSTGRES_SCHEMA"
    POSTGRES_SINGLE_ROW_TRACKING = "SINGLE_ROW_TRACKING"
    CREATE_TABLE = "CREATE_TABLE"

    aggregate_recorder_class = PostgresAggregateRecorder
    application_recorder_class = PostgresApplicationRecorder
    tracking_recorder_class = PostgresTrackingRecorder
    process_recorder_class = PostgresProcessRecorder

    def __init__(self, env: Environment | EnvType | None):
        super().__init__(env)
        dbname = self.env.get(self.POSTGRES_DBNAME)
        if dbname is None:
            msg = (
                "Postgres database name not found "
                "in environment with key "
                f"'{self.POSTGRES_DBNAME}'"
            )
            # TODO: Indicate both keys here, also for other environment variables.
            # ) + " or ".join(
            #   [f"'{key}'" for key in self.env.create_keys(self.POSTGRES_DBNAME)]
            # )
            raise OSError(msg)

        host = self.env.get(self.POSTGRES_HOST)
        if host is None:
            msg = (
                "Postgres host not found "
                "in environment with key "
                f"'{self.POSTGRES_HOST}'"
            )
            raise OSError(msg)

        port = self.env.get(self.POSTGRES_PORT) or "5432"

        user = self.env.get(self.POSTGRES_USER)
        if user is None:
            msg = (
                "Postgres user not found "
                "in environment with key "
                f"'{self.POSTGRES_USER}'"
            )
            raise OSError(msg)

        get_password_func = None
        get_password_topic = self.env.get(self.POSTGRES_GET_PASSWORD_TOPIC)
        if not get_password_topic:
            password = self.env.get(self.POSTGRES_PASSWORD)
            if password is None:
                msg = (
                    "Postgres password not found "
                    "in environment with key "
                    f"'{self.POSTGRES_PASSWORD}'"
                )
                raise OSError(msg)
        else:
            get_password_func = resolve_topic(get_password_topic)
            password = ""

        connect_timeout = 30
        connect_timeout_str = self.env.get(self.POSTGRES_CONNECT_TIMEOUT)
        if connect_timeout_str:
            try:
                connect_timeout = int(connect_timeout_str)
            except ValueError:
                msg = (
                    "Postgres environment value for key "
                    f"'{self.POSTGRES_CONNECT_TIMEOUT}' is invalid. "
                    "If set, an integer or empty string is expected: "
                    f"'{connect_timeout_str}'"
                )
                raise OSError(msg) from None

        idle_in_transaction_session_timeout_str = (
            self.env.get(self.POSTGRES_IDLE_IN_TRANSACTION_SESSION_TIMEOUT) or "5"
        )

        try:
            idle_in_transaction_session_timeout = int(
                idle_in_transaction_session_timeout_str
            )
        except ValueError:
            msg = (
                "Postgres environment value for key "
                f"'{self.POSTGRES_IDLE_IN_TRANSACTION_SESSION_TIMEOUT}' is invalid. "
                "If set, an integer or empty string is expected: "
                f"'{idle_in_transaction_session_timeout_str}'"
            )
            raise OSError(msg) from None

        pool_size = 5
        pool_size_str = self.env.get(self.POSTGRES_POOL_SIZE)
        if pool_size_str:
            try:
                pool_size = int(pool_size_str)
            except ValueError:
                msg = (
                    "Postgres environment value for key "
                    f"'{self.POSTGRES_POOL_SIZE}' is invalid. "
                    "If set, an integer or empty string is expected: "
                    f"'{pool_size_str}'"
                )
                raise OSError(msg) from None

        pool_max_overflow = 10
        pool_max_overflow_str = self.env.get(self.POSTGRES_MAX_OVERFLOW)
        if pool_max_overflow_str:
            try:
                pool_max_overflow = int(pool_max_overflow_str)
            except ValueError:
                msg = (
                    "Postgres environment value for key "
                    f"'{self.POSTGRES_MAX_OVERFLOW}' is invalid. "
                    "If set, an integer or empty string is expected: "
                    f"'{pool_max_overflow_str}'"
                )
                raise OSError(msg) from None

        max_waiting = 0
        max_waiting_str = self.env.get(self.POSTGRES_MAX_WAITING)
        if max_waiting_str:
            try:
                max_waiting = int(max_waiting_str)
            except ValueError:
                msg = (
                    "Postgres environment value for key "
                    f"'{self.POSTGRES_MAX_WAITING}' is invalid. "
                    "If set, an integer or empty string is expected: "
                    f"'{max_waiting_str}'"
                )
                raise OSError(msg) from None

        conn_max_age = 60 * 60.0
        conn_max_age_str = self.env.get(self.POSTGRES_CONN_MAX_AGE)
        if conn_max_age_str:
            try:
                conn_max_age = float(conn_max_age_str)
            except ValueError:
                msg = (
                    "Postgres environment value for key "
                    f"'{self.POSTGRES_CONN_MAX_AGE}' is invalid. "
                    "If set, a float or empty string is expected: "
                    f"'{conn_max_age_str}'"
                )
                raise OSError(msg) from None

        pre_ping = strtobool(self.env.get(self.POSTGRES_PRE_PING) or "no")

        lock_timeout_str = self.env.get(self.POSTGRES_LOCK_TIMEOUT) or "0"

        try:
            lock_timeout = int(lock_timeout_str)
        except ValueError:
            msg = (
                "Postgres environment value for key "
                f"'{self.POSTGRES_LOCK_TIMEOUT}' is invalid. "
                "If set, an integer or empty string is expected: "
                f"'{lock_timeout_str}'"
            )
            raise OSError(msg) from None

        schema = self.env.get(self.POSTGRES_SCHEMA) or ""

        single_row_tracking = strtobool(
            self.env.get(self.POSTGRES_SINGLE_ROW_TRACKING, "t")
        )

        self.datastore = PostgresDatastore(
            dbname=dbname,
            host=host,
            port=port,
            user=user,
            password=password,
            connect_timeout=connect_timeout,
            idle_in_transaction_session_timeout=idle_in_transaction_session_timeout,
            pool_size=pool_size,
            max_overflow=pool_max_overflow,
            max_waiting=max_waiting,
            conn_max_age=conn_max_age,
            pre_ping=pre_ping,
            lock_timeout=lock_timeout,
            schema=schema,
            get_password_func=get_password_func,
            single_row_tracking=single_row_tracking,
        )

    def env_create_table(self) -> bool:
        return strtobool(self.env.get(self.CREATE_TABLE) or "yes")

    def aggregate_recorder(self, purpose: str = "events") -> AggregateRecorder:
        prefix = self.env.name.lower() or "stored"
        events_table_name = prefix + "_" + purpose
        recorder = type(self).aggregate_recorder_class(
            datastore=self.datastore,
            events_table_name=events_table_name,
        )
        if self.env_create_table():
            recorder.create_table()
        return recorder

    def application_recorder(self) -> ApplicationRecorder:
        prefix = self.env.name.lower() or "stored"
        events_table_name = prefix + "_events"
        application_recorder_topic = self.env.get(self.APPLICATION_RECORDER_TOPIC)
        if application_recorder_topic:
            application_recorder_class: type[PostgresApplicationRecorder] = (
                resolve_topic(application_recorder_topic)
            )
            assert issubclass(application_recorder_class, PostgresApplicationRecorder)
        else:
            application_recorder_class = type(self).application_recorder_class

        recorder = application_recorder_class(
            datastore=self.datastore,
            events_table_name=events_table_name,
        )
        if self.env_create_table():
            recorder.create_table()
        return recorder

    def tracking_recorder(
        self, tracking_recorder_class: type[TPostgresTrackingRecorder] | None = None
    ) -> TPostgresTrackingRecorder:
        prefix = self.env.name.lower() or "notification"
        tracking_table_name = prefix + "_tracking"
        if tracking_recorder_class is None:
            tracking_recorder_topic = self.env.get(self.TRACKING_RECORDER_TOPIC)
            if tracking_recorder_topic:
                tracking_recorder_class = resolve_topic(tracking_recorder_topic)
            else:
                tracking_recorder_class = cast(
                    "type[TPostgresTrackingRecorder]",
                    type(self).tracking_recorder_class,
                )
        assert tracking_recorder_class is not None
        assert issubclass(tracking_recorder_class, PostgresTrackingRecorder)
        recorder = tracking_recorder_class(
            datastore=self.datastore,
            tracking_table_name=tracking_table_name,
        )
        if self.env_create_table():
            recorder.create_table()
        return recorder

    def process_recorder(self) -> ProcessRecorder:
        prefix = self.env.name.lower() or "stored"
        events_table_name = prefix + "_events"
        prefix = self.env.name.lower() or "notification"
        tracking_table_name = prefix + "_tracking"
        process_recorder_topic = self.env.get(self.PROCESS_RECORDER_TOPIC)
        if process_recorder_topic:
            process_recorder_class: type[PostgresTrackingRecorder] = resolve_topic(
                process_recorder_topic
            )
            assert issubclass(process_recorder_class, PostgresProcessRecorder)
        else:
            process_recorder_class = type(self).process_recorder_class

        recorder = process_recorder_class(
            datastore=self.datastore,
            events_table_name=events_table_name,
            tracking_table_name=tracking_table_name,
        )
        if self.env_create_table():
            recorder.create_table()
        return recorder

    def close(self) -> None:
        with contextlib.suppress(AttributeError):
            self.datastore.close()


Factory = PostgresFactory
