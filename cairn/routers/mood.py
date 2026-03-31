from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Optional
from cairn.database import get_db
from cairn.models.mood import Mood
from cairn.models.entry import Entry, EntryType, Tag
from cairn.schemas.mood import MoodEntryCreate, MoodEntryRead
from cairn.routers.get_tags import _get_or_create_tag

router = APIRouter(prefix="/mood", tags=["mood"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   POST /mood               — log a mood check-in
#   GET  /mood               — list (filter: tag, date)
#   GET  /mood/{id}          — single entry
#
# Models:  cairn/models/mood.py     (Mood)
# Schemas: cairn/schemas/mood.py    (MoodEntryCreate, MoodEntryRead, MoodDetails)

@router.post("/", response_model=MoodEntryRead, status_code=201)
def create_mood(payload: MoodEntryCreate, db: Session = Depends(get_db)):
    entry = Entry(
        type=EntryType.mood,
        timestamp=payload.timestamp,
        notes=payload.notes,
    )
    entry.tags = _get_or_create_tag(db, payload.tags)
    entry.mood = Mood(**payload.mood.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/", response_model=list[MoodEntryRead])
def list_mood(
    tag: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Entry).filter(Entry.type == EntryType.mood)
    if tag:
        q = q.join(Entry.tags).filter(Tag.name == tag)
    if from_date:
        q = q.filter(Entry.timestamp >= from_date)
    if to_date:
        q = q.filter(Entry.timestamp <= to_date)
    return q.order_by(Entry.timestamp.desc()).offset(offset).limit(limit).all()

@router.get("/{entry_id}", response_model=MoodEntryRead)
def get_mood(entry_id: int, db: Session = Depends(get_db)):
    entry = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.type == EntryType.mood)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Mood not found")
    return entry
