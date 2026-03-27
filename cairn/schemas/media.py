from typing import Optional
from pydantic import BaseModel
from cairn.models.media import MediaType, MediaStatus
from cairn.schemas.entry import EntryReadBase, EntryCreateBase


class MediaDetails(BaseModel):
    title: str
    media_type: MediaType
    creator: Optional[str] = None
    status: Optional[MediaStatus] = None
    rating: Optional[int] = None  # 1–10

    model_config = {"from_attributes": True}


class MediaEntryCreate(EntryCreateBase):
    media: MediaDetails


class MediaEntryRead(EntryReadBase):
    media: MediaDetails
