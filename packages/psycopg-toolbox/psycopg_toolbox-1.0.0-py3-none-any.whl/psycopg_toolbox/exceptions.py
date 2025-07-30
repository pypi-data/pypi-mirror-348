"""Custom exceptions for psycopg-toolbox."""


class AlreadyExistsError(Exception):
    """Raised when attempting to create a database, user or role that already exists."""

    pass
