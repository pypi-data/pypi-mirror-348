"""A logging cursor implementation for psycopg-toolbox.

This module provides a LoggingCursor class that extends psycopg's AsyncCursor
and logs all executed queries and their parameters, but skips logging parameters
if the query contains sensitive words.
"""

import logging
import re
from typing import Any, Generic, Iterable, Mapping, Sequence, TypeVar

from psycopg.cursor_async import AsyncCursor
from psycopg.sql import SQL, Composed

logger = logging.getLogger(__name__)

T = TypeVar("T")


class LoggingCursor(AsyncCursor[T], Generic[T]):
    """A cursor that logs queries and parameters, but skips params if query is sensitive.

    If the query contains a banned word (e.g., password, ssn, credit card),
    parameters are not logged at all.
    """

    # Banned words for sensitive queries
    _BANNED_WORDS = [
        "password",
        "passwd",
        "pwd",
        "token",
        "secret",
        "key",
        "ssn",
        "social security",
        "credit card",
        "cc",
        "card number",
    ]
    _BANNED_WORDS_PATTERN = re.compile(
        r"|".join(re.escape(word) for word in _BANNED_WORDS), re.IGNORECASE
    )

    async def execute(
        self,
        query: str | bytes | SQL | Composed,
        params: Sequence[Any] | Mapping[str, Any] | None = None,
        *,
        prepare: bool | None = None,
        binary: bool | None = None,
    ) -> "LoggingCursor[T]":
        """Execute a query and log it unless it contains sensitive data."""
        logger.info("Executing query: %s", query)
        if params is not None:
            if self._BANNED_WORDS_PATTERN.search(str(query)):
                logger.info("Parameters not logged due to sensitive query.")
            else:
                logger.info("With parameters: %s", params)
        return await super().execute(query, params, prepare=prepare, binary=binary)

    async def executemany(
        self,
        query: str | bytes | SQL | Composed,
        params_seq: Iterable[Sequence[Any] | Mapping[str, Any]],
        *,
        returning: bool = False,
    ) -> None:
        """Execute a query multiple times and log it unless it contains sensitive data."""
        logger.info("Executing query multiple times: %s", query)
        if params_seq is not None:
            if self._BANNED_WORDS_PATTERN.search(str(query)):
                logger.info("Parameters sequence not logged due to sensitive query.")
            else:
                logger.info("With parameters sequence: %s", params_seq)
        await super().executemany(query, params_seq, returning=returning)
