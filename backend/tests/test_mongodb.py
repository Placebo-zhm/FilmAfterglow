from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.db.mongodb import MongoDB


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_mongodb_connect_and_disconnect() -> None:
    client = MagicMock()
    client.admin.command = AsyncMock()
    client.close = AsyncMock()

    database = MongoDB()
    with patch("app.db.mongodb.AsyncMongoClient", return_value=client):
        await database.connect()

    client.admin.command.assert_awaited_once_with("ping")
    assert database.client is client

    await database.disconnect()

    client.close.assert_awaited_once()
    with pytest.raises(RuntimeError, match="has not been initialized"):
        _ = database.client
