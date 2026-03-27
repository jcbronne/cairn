from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from cairn.database import get_db
from cairn.models.entry import Entry, EntryType, Tag
from cairn.schemas.entry import EntryRead

router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("/", response_model=list[EntryRead])
def list_entries(
    type: Optional[EntryType] = None,
    tag: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """Timeline view — query across all entry types."""
    q = db.query(Entry)
    if type:
        q = q.filter(Entry.type == type)
    if tag:
        q = q.join(Entry.tags).filter(Tag.name == tag)
    if from_date:
        q = q.filter(Entry.timestamp >= from_date)
    if to_date:
        q = q.filter(Entry.timestamp <= to_date)
    return q.order_by(Entry.timestamp.desc()).offset(offset).limit(limit).all()
