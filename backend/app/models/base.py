from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class MongoModel(BaseModel):
    """Base model shared by MongoDB documents."""

    id: UUID = Field(default_factory=uuid4, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    def to_document(self) -> dict:
        """Return a MongoDB-ready document using database field names."""
        return self.model_dump(by_alias=True)
