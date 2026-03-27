from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cairn.database import get_db
from cairn.models.entry import Entry, EntryType, Tag
from cairn.models.hike import Hike
from cairn.schemas.hike import HikeEntryCreate, HikeEntryRead

router = APIRouter(prefix="/hikes", tags=["hikes"])


def _get_or_create_tag(db: Session, name: str) -> Tag:
    tag = db.query(Tag).filter(Tag.name == name).first()
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
    return tag


@router.post("/", response_model=HikeEntryRead, status_code=201)
def create_hike(payload: HikeEntryCreate, db: Session = Depends(get_db)):
    entry = Entry(
        type=EntryType.hike,
        timestamp=payload.timestamp,
        notes=payload.notes,
    )
    for tag_name in payload.tags:
        entry.tags.append(_get_or_create_tag(db, tag_name))
    entry.hike = Hike(**payload.hike.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=list[HikeEntryRead])
def list_hikes(
    tag: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Entry).filter(Entry.type == EntryType.hike)
    if tag:
        q = q.join(Entry.tags).filter(Tag.name == tag)
    if from_date:
        q = q.filter(Entry.timestamp >= from_date)
    if to_date:
        q = q.filter(Entry.timestamp <= to_date)
    return q.order_by(Entry.timestamp.desc()).offset(offset).limit(limit).all()


@router.get("/{entry_id}", response_model=HikeEntryRead)
def get_hike(entry_id: int, db: Session = Depends(get_db)):
    entry = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.type == EntryType.hike)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Hike not found")
    return entry
