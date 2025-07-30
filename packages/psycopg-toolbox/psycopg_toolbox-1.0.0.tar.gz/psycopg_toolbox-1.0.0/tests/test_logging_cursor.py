"""Tests for LoggingCursor."""

import logging

import pytest
from _pytest.logging import LogCaptureFixture

from psycopg_toolbox import LoggingConnection


@pytest.mark.asyncio
async def test_execute_with_sensitive_data(
    psycopg_toolbox_empty_db: LoggingConnection, caplog: LogCaptureFixture
) -> None:
    """Test execute method skips logging params for sensitive queries."""
    caplog.set_level(logging.INFO)
    test_query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    test_params = ["user@example.com", "secret123"]
    async with psycopg_toolbox_empty_db.cursor() as cur:
        await cur.execute(
            "CREATE TABLE IF NOT EXISTS users (email text, password text)"
        )
        await cur.execute(test_query, test_params)
        assert f"Executing query: {test_query}" in caplog.text
        assert "Parameters not logged due to sensitive query." in caplog.text
        assert "user@example.com" not in caplog.text
        assert "secret123" not in caplog.text


@pytest.mark.asyncio
async def test_executemany_with_sensitive_data(
    psycopg_toolbox_empty_db: LoggingConnection, caplog: LogCaptureFixture
) -> None:
    """Test executemany skips logging params for sensitive queries."""
    caplog.set_level(logging.INFO)
    test_query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    test_params = [
        ("user1@example.com", "pass1"),
        ("user2@example.com", "pass2"),
    ]
    async with psycopg_toolbox_empty_db.cursor() as cur:
        await cur.execute(
            "CREATE TABLE IF NOT EXISTS users (email text, password text)"
        )
        await cur.executemany(test_query, test_params)
        assert f"Executing query multiple times: {test_query}" in caplog.text
        assert "Parameters sequence not logged due to sensitive query." in caplog.text
        assert "user1@example.com" not in caplog.text
        assert "user2@example.com" not in caplog.text
        assert "pass1" not in caplog.text
        assert "pass2" not in caplog.text


@pytest.mark.asyncio
async def test_dict_parameter_sensitive_query(
    psycopg_toolbox_empty_db: LoggingConnection, caplog: LogCaptureFixture
) -> None:
    """Test that parameters are not logged if query contains a banned word."""
    caplog.set_level(logging.INFO)
    test_query = "INSERT INTO users (email, ssn, credit_card) VALUES (%s, %s, %s)"
    test_params = [
        "user@example.com",
        "123-45-6789",
        "4111-1111-1111-1111",
    ]
    await psycopg_toolbox_empty_db.execute(
        "CREATE TABLE IF NOT EXISTS users (email text, ssn text, credit_card text)"
    )
    await psycopg_toolbox_empty_db.execute(test_query, test_params)
    assert f"Executing query: {test_query}" in caplog.text
    assert "Parameters not logged due to sensitive query." in caplog.text
    assert "user@example.com" not in caplog.text
    assert "123-45-6789" not in caplog.text
    assert "4111-1111-1111-1111" not in caplog.text


@pytest.mark.asyncio
async def test_execute_with_non_sensitive_query(
    psycopg_toolbox_empty_db: LoggingConnection, caplog: LogCaptureFixture
) -> None:
    """Test that parameters are logged for non-sensitive queries."""
    caplog.set_level(logging.INFO)
    test_query = "INSERT INTO users (email, phone) VALUES (%s, %s)"
    test_params = ["user@example.com", "123-456-7890"]
    await psycopg_toolbox_empty_db.execute(
        "CREATE TABLE IF NOT EXISTS users (email text, phone text)"
    )
    await psycopg_toolbox_empty_db.execute(test_query, test_params)
    assert f"Executing query: {test_query}" in caplog.text
    assert f"With parameters: {test_params}" in caplog.text
    assert "user@example.com" in caplog.text
    assert "123-456-7890" in caplog.text


@pytest.mark.asyncio
async def test_executemany_with_non_sensitive_query(
    psycopg_toolbox_empty_db: LoggingConnection, caplog: LogCaptureFixture
) -> None:
    """Test that parameters are logged for non-sensitive queries with executemany."""
    caplog.set_level(logging.INFO)
    test_query = "INSERT INTO users (email, phone) VALUES (%s, %s)"
    test_params = [
        ("user1@example.com", "123-456-7890"),
        ("user2@example.com", "987-654-3210"),
    ]
    async with psycopg_toolbox_empty_db.cursor() as cur:
        await cur.execute("CREATE TABLE IF NOT EXISTS users (email text, phone text)")
        await cur.executemany(test_query, test_params)
        assert f"Executing query multiple times: {test_query}" in caplog.text
        assert f"With parameters sequence: {test_params}" in caplog.text
        assert "user1@example.com" in caplog.text
        assert "987-654-3210" in caplog.text
