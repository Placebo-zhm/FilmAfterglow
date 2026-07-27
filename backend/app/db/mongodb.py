from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings


class MongoDB:
    """Own the application-wide MongoDB client and connection pool."""

    def __init__(self) -> None:
        self._client: AsyncMongoClient[dict] | None = None

    @property
    def client(self) -> AsyncMongoClient[dict]:
        if self._client is None:
            raise RuntimeError("MongoDB client has not been initialized")
        return self._client

    @property
    def database(self) -> AsyncDatabase[dict]:
        return self.client[settings.mongodb_database]

    async def connect(self) -> None:
        if self._client is not None:
            return

        client: AsyncMongoClient[dict] = AsyncMongoClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=settings.mongodb_server_selection_timeout_ms,
            uuidRepresentation="standard",
        )
        try:
            await client.admin.command("ping")
        except Exception:
            await client.close()
            raise
        self._client = client

    async def disconnect(self) -> None:
        if self._client is None:
            return
        await self._client.close()
        self._client = None


mongodb = MongoDB()


def get_database() -> AsyncDatabase[dict]:
    """FastAPI dependency that provides the configured application database."""
    return mongodb.database
