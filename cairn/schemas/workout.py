from typing import Optional
from pydantic import BaseModel
from cairn.schemas.entry import EntryReadBase, EntryCreateBase


class WorkoutDetails(BaseModel):
    workout_type: str  # run, lift, yoga, swim, etc.
    duration_min: Optional[int] = None
    distance_km: Optional[float] = None

    model_config = {"from_attributes": True}


class WorkoutEntryCreate(EntryCreateBase):
    workout: WorkoutDetails


class WorkoutEntryRead(EntryReadBase):
    workout: WorkoutDetails
