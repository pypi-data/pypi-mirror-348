"""Tests for LoggingConnection."""

import logging

import pytest
from _pytest.logging import LogCaptureFixture

from psycopg_toolbox import LoggingConnection


@pytest.mark.asyncio
async def test_connection_creation_logged(
    psycopg_toolbox_empty_db: LoggingConnection, caplog: LogCaptureFixture
) -> None:
    """Test that connection creation is logged."""
    caplog.set_level(logging.INFO)
    info = psycopg_toolbox_empty_db.info
    conn = await LoggingConnection.connect(
        dbname=info.dbname,
        user=info.user,
        password=info.password,
        host=info.host,
        port=info.port,
    )
    try:
        assert f"Connection created: {conn.info.host}:{conn.info.port}" in caplog.text
    finally:
        await conn.close()


@pytest.mark.asyncio
async def test_connection_closure_logged(
    psycopg_toolbox_empty_db: LoggingConnection, caplog: LogCaptureFixture
) -> None:
    """Test that connection closure is logged."""
    caplog.set_level(logging.INFO)
    info = psycopg_toolbox_empty_db.info
    conn = await LoggingConnection.connect(
        dbname=info.dbname,
        user=info.user,
        password=info.password,
        host=info.host,
        port=info.port,
    )
    await conn.close()
    assert f"Connection closed: {info.host}:{info.port}" in caplog.text
