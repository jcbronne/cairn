from typing import Optional
from pydantic import BaseModel
from cairn.schemas.entry import EntryReadBase, EntryCreateBase


class HikeDetails(BaseModel):
    trail_name: Optional[str] = None
    location: Optional[str] = None
    distance_km: Optional[float] = None
    elevation_gain_m: Optional[float] = None
    duration_min: Optional[int] = None

    model_config = {"from_attributes": True}


class HikeEntryCreate(EntryCreateBase):
    hike: HikeDetails


class HikeEntryRead(EntryReadBase):
    hike: HikeDetails
