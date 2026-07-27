from datetime import UTC
from uuid import UUID

from app.models.user import User


def test_user_document_uses_uuid_as_mongodb_id() -> None:
    user = User(
        username="admin",
        email="admin@example.com",
        password_hash="hashed-password",
    )

    document = user.to_document()

    assert isinstance(document["_id"], UUID)
    assert "id" not in document
    assert user.role == "admin"
    assert user.is_active is True
    assert user.last_login_at is None
    assert user.created_at.tzinfo is UTC
    assert user.updated_at.tzinfo is UTC


def test_user_accepts_mongodb_id_alias() -> None:
    user = User(
        _id="9f8e746b-80d4-4c91-8842-725c9b823b23",
        username="photographer",
        email="photo@example.com",
        password_hash="hashed-password",
        role="admin",
    )

    assert user.id == UUID("9f8e746b-80d4-4c91-8842-725c9b823b23")
