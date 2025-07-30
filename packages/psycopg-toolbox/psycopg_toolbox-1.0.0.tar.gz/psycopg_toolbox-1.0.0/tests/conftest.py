"""Test configuration for psycopg-toolbox."""

import asyncio
import os
from typing import Generator

import pytest
from psycopg import AsyncConnection

from psycopg_toolbox import drop_database

# Declare our test fixtures as a plugin
pytest_plugins = ["psycopg_toolbox.testfixtures"]


@pytest.fixture(scope="session", autouse=True)
def isolated_env(
    psycopg_toolbox_db_name: str, db_config
) -> Generator[None, None, None]:
    """Isolate the test environment from the system environment.

    This fixture:
    1. Saves the current environment
    2. Clears all environment variables
    3. Restores the original environment after the test

    Args:
        psycopg_toolbox_db_name: Ensures worker ID is captured before environment isolation
        db_config: Ensures database configuration is read before environment isolation
    """
    # Save the current environment
    original_env = dict(os.environ)

    # Clear all environment variables
    os.environ.clear()

    yield

    # Restore the original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture(scope="session", autouse=True)
def cleanup_psycopg_toolbox_test_dbs(db_config) -> None:
    """Remove any leftover test databases with the prefix 'psycopg_toolbox_test_' before the test session starts."""

    async def _cleanup():
        # Connect to the default database
        async with await AsyncConnection.connect(
            dbname="postgres",
            user=db_config.user,
            password=db_config.password,
            host=db_config.host,
            port=db_config.port,
        ) as conn:
            # Find all test databases
            cur = await conn.execute(
                """
                SELECT datname FROM pg_database
                WHERE datname LIKE 'psycopg_toolbox_test_%'
                AND datistemplate = false
                """
            )
            dbs = [row[0] for row in await cur.fetchall()]
            for db in dbs:
                try:
                    await drop_database(conn, db, ignore_missing=True)
                except Exception:
                    pass  # Ignore errors, best effort cleanup

    asyncio.get_event_loop().run_until_complete(_cleanup())
