from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Optional
from cairn.database import get_db
from cairn.models.workout import Workout
from cairn.models.entry import Entry, EntryType, Tag
from cairn.schemas.workout import WorkoutEntryCreate, WorkoutEntryRead
from cairn.routers.get_tags import _get_or_create_tag

router = APIRouter(prefix="/workouts", tags=["workouts"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   POST /workouts           — log a workout
#   GET  /workouts           — list (filter: tag, date, workout_type)
#   GET  /workouts/{id}      — single entry
#
# Models:  cairn/models/workout.py  (Workout)
# Schemas: cairn/schemas/workout.py (WorkoutEntryCreate, WorkoutEntryRead, WorkoutDetails)

@router.post("/", response_model=WorkoutEntryRead, status_code=201)
def create_workout(payload: WorkoutEntryCreate, db: Session = Depends(get_db)):
    entry = Entry(
        type=EntryType.workout,
        timestamp=payload.timestamp,
        notes=payload.notes,
    )
    entry.tags = _get_or_create_tag(db, payload.tags)
    entry.workout = Workout(**payload.workout.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/", response_model=list[WorkoutEntryRead])
def list_workout(
    tag: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Entry).filter(Entry.type == EntryType.workout)
    if tag:
        q = q.join(Entry.tags).filter(Tag.name == tag)
    if from_date:
        q = q.filter(Entry.timestamp >= from_date)
    if to_date:
        q = q.filter(Entry.timestamp <= to_date)
    return q.order_by(Entry.timestamp.desc()).offset(offset).limit(limit).all()

@router.get("/{entry_id}", response_model=WorkoutEntryRead)
def get_workout(entry_id: int, db: Session = Depends(get_db)):
    entry = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.type == EntryType.workout)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Workout not found")
    return entry
