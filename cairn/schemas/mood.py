from typing import Optional
from pydantic import BaseModel
from cairn.schemas.entry import EntryReadBase, EntryCreateBase


class MoodDetails(BaseModel):
    score: int  # 1–10
    energy: Optional[int] = None  # 1–5

    model_config = {"from_attributes": True}


class MoodEntryCreate(EntryCreateBase):
    mood: MoodDetails


class MoodEntryRead(EntryReadBase):
    mood: MoodDetails
