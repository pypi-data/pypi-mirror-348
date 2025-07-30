"""psycopg-toolbox package."""

from psycopg_toolbox.contextmanagers import (
    autocommit,
    switch_role,
    obtain_advisory_lock,
)
from psycopg_toolbox.logging_connection import LoggingConnection
from psycopg_toolbox.logging_cursor import LoggingCursor
from psycopg_toolbox.query_helpers import (
    create_database,
    database_exists,
    drop_database,
)
from psycopg_toolbox.exceptions import AlreadyExistsError

__all__ = [
    "autocommit",
    "switch_role",
    "obtain_advisory_lock",
    "LoggingConnection",
    "LoggingCursor",
    "create_database",
    "database_exists",
    "drop_database",
    "AlreadyExistsError",
]
