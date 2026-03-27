from typing import Optional
from pydantic import BaseModel
from cairn.models.game import GameStatus
from cairn.schemas.entry import EntryReadBase, EntryCreateBase


class GameDetails(BaseModel):
    title: str
    platform: Optional[str] = None
    status: Optional[GameStatus] = None
    hours: Optional[float] = None
    rating: Optional[int] = None  # 1–10

    model_config = {"from_attributes": True}


class GameEntryCreate(EntryCreateBase):
    game: GameDetails


class GameEntryRead(EntryReadBase):
    game: GameDetails
