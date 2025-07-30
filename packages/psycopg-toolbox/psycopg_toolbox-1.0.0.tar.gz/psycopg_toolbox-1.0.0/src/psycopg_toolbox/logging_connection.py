"""A logging connection implementation for psycopg-toolbox.

This module provides a LoggingConnection class that extends psycopg's AsyncConnection
to log when connections are created and closed, and uses LoggingCursor as the default cursor_factory.
"""

import logging
from typing import Any, Self, Type

from psycopg import AsyncConnection
from psycopg.cursor_async import AsyncCursor
from psycopg.rows import AsyncRowFactory, Row

from psycopg_toolbox.logging_cursor import LoggingCursor

logger = logging.getLogger(__name__)


class LoggingConnection(AsyncConnection[Row]):
    """A connection that logs when it is created and closed, and uses LoggingCursor by default."""

    async def close(self) -> None:
        """Close the connection and log its closure."""
        logger.info("Connection closed: %s:%s", self.info.host, self.info.port)
        await super().close()

    @classmethod
    async def connect(
        cls,
        conninfo: str = "",
        *,
        autocommit: bool = False,
        prepare_threshold: int | None = None,
        context: Any | None = None,
        row_factory: AsyncRowFactory[Row] | None = None,
        cursor_factory: Type[AsyncCursor[Row]] | None = None,
        **kwargs: str | int | None,
    ) -> Self:
        """Create a new connection with LoggingCursor as the default cursor_factory.

        Args:
            conninfo: Connection string
            autocommit: Whether to enable autocommit mode
            prepare_threshold: Number of times a query must be executed before it is prepared
            context: Adaptation context (type Any for compatibility)
            row_factory: Factory for creating row objects
            cursor_factory: Factory for creating cursor objects
            **kwargs: Additional connection parameters
        """
        if cursor_factory is None:
            cursor_factory = LoggingCursor[Row]

        conn = await super().connect(
            conninfo=conninfo,
            autocommit=autocommit,
            prepare_threshold=prepare_threshold,
            context=context,
            row_factory=row_factory,
            cursor_factory=cursor_factory,
            **kwargs,
        )

        logger.info("Connection created: %s:%s", conn.info.host, conn.info.port)
        return conn
