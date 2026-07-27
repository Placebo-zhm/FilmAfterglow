from datetime import UTC, datetime
from typing import ClassVar

from pydantic import Field

from app.models.base import MongoModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(MongoModel):
    """User account document stored in the ``users`` collection."""

    username: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=320)
    password_hash: str = Field(min_length=1, repr=False)
    role: str = Field(default="admin", min_length=1, max_length=50)
    is_active: bool = True
    last_login_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    collection_name: ClassVar[str] = "users"
