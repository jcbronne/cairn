from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Optional
from cairn.database import get_db
from cairn.models.media import Media
from cairn.models.entry import Entry, EntryType, Tag
from cairn.schemas.media import MediaEntryCreate, MediaEntryRead
from cairn.routers.get_tags import _get_or_create_tag

router = APIRouter(prefix="/media", tags=["media"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   POST /media              — log a book, film, TV show, podcast, or album
#   GET  /media              — list (filter: tag, date, media_type, status)
#   GET  /media/{id}         — single entry
#
# Models:  cairn/models/media.py    (Media, MediaType, MediaStatus)
# Schemas: cairn/schemas/media.py   (MediaEntryCreate, MediaEntryRead, MediaDetails)

@router.post("/", response_model=MediaEntryRead, status_code=201)
def create_media(payload: MediaEntryCreate, db: Session = Depends(get_db)):
    entry = Entry(
        type=EntryType.media,
        timestamp=payload.timestamp,
        notes=payload.notes,
    )
    entry.tags = _get_or_create_tag(db, payload.tags)
    entry.media = Media(**payload.media.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/", response_model=list[MediaEntryRead])
def list_media(
    tag: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Entry).filter(Entry.type == EntryType.media)
    if tag:
        q = q.join(Entry.tags).filter(Tag.name == tag)
    if from_date:
        q = q.filter(Entry.timestamp >= from_date)
    if to_date:
        q = q.filter(Entry.timestamp <= to_date)
    return q.order_by(Entry.timestamp.desc()).offset(offset).limit(limit).all()

@router.get("/{entry_id}", response_model=MediaEntryRead)
def get_media(entry_id: int, db: Session = Depends(get_db)):
    entry = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.type == EntryType.media)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Media not found")
    return entry
