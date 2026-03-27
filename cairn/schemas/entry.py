from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from cairn.models.entry import EntryType


class EntryReadBase(BaseModel):
    """Base for all entry read schemas — inherit and add your detail field."""

    id: int
    type: EntryType
    timestamp: datetime
    notes: Optional[str] = None
    tags: list[str] = []
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("tags", mode="before")
    @classmethod
    def coerce_tags(cls, v):
        if not v:
            return []
        if isinstance(v[0], str):
            return v
        return [item.name for item in v]  # SQLAlchemy Tag objects → strings


class EntryCreateBase(BaseModel):
    """Base for all entry create schemas — inherit and add your detail field."""

    timestamp: datetime
    notes: Optional[str] = None
    tags: list[str] = []


class EntryRead(EntryReadBase):
    """Flat entry — used by the cross-type timeline endpoint."""
    pass
