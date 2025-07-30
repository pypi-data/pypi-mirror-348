"""Tests for context managers in psycopg-toolbox."""

import pytest
from psycopg.errors import Error

from psycopg_toolbox.contextmanagers import (
    autocommit,
    switch_role,
    obtain_advisory_lock,
)
from psycopg_toolbox.logging_connection import LoggingConnection


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial_autocommit,should_error",
    [
        (False, False),  # Start disabled, no error
        (True, False),  # Start enabled, no error
        (False, True),  # Start disabled, with error
        (True, True),  # Start enabled, with error
    ],
    ids=[
        "disabled_no_error",
        "enabled_no_error",
        "disabled_with_error",
        "enabled_with_error",
    ],
)
async def test_autocommit_context_manager(
    psycopg_toolbox_empty_db: LoggingConnection,
    initial_autocommit: bool,
    should_error: bool,
) -> None:
    """Test the autocommit context manager behavior.

    Tests all combinations of:
    - Initial autocommit state (enabled/disabled)
    - Normal execution vs error handling

    Args:
        psycopg_toolbox_empty_db: Test database connection
        initial_autocommit: Whether to start with autocommit enabled
        should_error: Whether to simulate an error during context execution
    """
    # Set initial state
    await psycopg_toolbox_empty_db.set_autocommit(initial_autocommit)
    assert psycopg_toolbox_empty_db.autocommit == initial_autocommit

    # Run the context manager
    if should_error:
        with pytest.raises(Error):
            async with autocommit(psycopg_toolbox_empty_db):
                assert psycopg_toolbox_empty_db.autocommit
                await psycopg_toolbox_empty_db.execute("SELECT 1/0")
    else:
        async with autocommit(psycopg_toolbox_empty_db):
            assert psycopg_toolbox_empty_db.autocommit

    # Verify final state matches initial state
    assert psycopg_toolbox_empty_db.autocommit == initial_autocommit


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "should_error",
    [False, True],
    ids=["no_error", "with_error"],
)
async def test_switch_role_context_manager(
    psycopg_toolbox_empty_db: LoggingConnection,
    should_error: bool,
) -> None:
    """Test the switch_role context manager behavior.

    Tests:
    - Role switching works correctly
    - Original role is restored after exit
    - Original role is restored even if an error occurs

    Args:
        psycopg_toolbox_empty_db: Test database connection
        should_error: Whether to simulate an error during context execution
    """
    # Get initial role
    result = await psycopg_toolbox_empty_db.execute("SELECT current_user")
    row = await result.fetchone()
    if row is None:
        raise RuntimeError("Failed to get current user")
    original_role = row[0]

    # Create a test role
    test_role = "psycopg_toolbox_test_role_switch"
    await psycopg_toolbox_empty_db.execute(f"DROP ROLE IF EXISTS {test_role}")
    await psycopg_toolbox_empty_db.execute(f"CREATE ROLE {test_role}")
    await psycopg_toolbox_empty_db.execute(f"GRANT {test_role} TO {original_role}")

    if should_error:
        with pytest.raises(Error):
            async with switch_role(psycopg_toolbox_empty_db, test_role) as yielded_role:
                assert yielded_role == original_role
                result = await psycopg_toolbox_empty_db.execute("SELECT current_user")
                row = await result.fetchone()
                if row is None:
                    raise RuntimeError("Failed to get current user")
                current_role = row[0]
                assert current_role == test_role
                await psycopg_toolbox_empty_db.execute("SELECT 1/0")
        # Rollback after error to reset transaction state
        await psycopg_toolbox_empty_db.rollback()
    else:
        async with switch_role(psycopg_toolbox_empty_db, test_role) as yielded_role:
            assert yielded_role == original_role
            result = await psycopg_toolbox_empty_db.execute("SELECT current_user")
            row = await result.fetchone()
            if row is None:
                raise RuntimeError("Failed to get current user")
            current_role = row[0]
            assert current_role == test_role

    # Verify final role matches initial role
    result = await psycopg_toolbox_empty_db.execute("SELECT current_user")
    row = await result.fetchone()
    if row is None:
        raise RuntimeError("Failed to get current user")
    final_role = row[0]
    assert final_role == original_role


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "blocking,should_error",
    [
        (True, False),  # Blocking, no error
        (False, False),  # Non-blocking, no error
        (True, True),  # Blocking, with error
        (False, True),  # Non-blocking, with error
    ],
    ids=[
        "blocking_no_error",
        "non_blocking_no_error",
        "blocking_with_error",
        "non_blocking_with_error",
    ],
)
async def test_obtain_advisory_lock_context_manager(
    psycopg_toolbox_empty_db: LoggingConnection,
    blocking: bool,
    should_error: bool,
) -> None:
    """Test the obtain_advisory_lock context manager behavior.

    Tests:
    - Lock acquisition works correctly
    - Lock is released after exit
    - Lock is released even if an error occurs
    - Non-blocking mode returns False if lock cannot be obtained

    Args:
        psycopg_toolbox_empty_db: Test database connection
        blocking: Whether to use blocking or non-blocking mode
        should_error: Whether to simulate an error during context execution
    """
    lock_name = "test_advisory_lock"

    if should_error:
        with pytest.raises(Error):
            async with obtain_advisory_lock(
                psycopg_toolbox_empty_db, lock_name, blocking
            ) as obtained:
                assert obtained
                await psycopg_toolbox_empty_db.execute("SELECT 1/0")
        # Rollback after error to reset connection state
        await psycopg_toolbox_empty_db.rollback()
    else:
        async with obtain_advisory_lock(
            psycopg_toolbox_empty_db, lock_name, blocking
        ) as obtained:
            assert obtained

    # Verify lock is released by trying to obtain it again
    async with obtain_advisory_lock(
        psycopg_toolbox_empty_db, lock_name, blocking
    ) as obtained:
        assert obtained


@pytest.mark.asyncio
async def test_obtain_advisory_lock_non_blocking_failure(
    psycopg_toolbox_empty_db: LoggingConnection,
) -> None:
    """Test that non-blocking mode returns False when lock cannot be obtained.

    Args:
        psycopg_toolbox_empty_db: Test database connection
    """
    lock_name = "test_advisory_lock"

    # Create a second connection to hold the lock
    conn2 = await LoggingConnection.connect(
        host=psycopg_toolbox_empty_db.info.host,
        port=psycopg_toolbox_empty_db.info.port,
        user=psycopg_toolbox_empty_db.info.user,
        password=psycopg_toolbox_empty_db.info.password,
        dbname=psycopg_toolbox_empty_db.info.dbname,
    )
    try:
        # Obtain lock with second connection
        async with obtain_advisory_lock(conn2, lock_name, blocking=True) as obtained:
            assert obtained

            # Try to obtain lock with first connection in non-blocking mode
            async with obtain_advisory_lock(
                psycopg_toolbox_empty_db, lock_name, blocking=False
            ) as obtained:
                assert not obtained
    finally:
        await conn2.close()
