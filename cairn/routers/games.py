from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Optional
from cairn.database import get_db
from cairn.models.game import Game
from cairn.models.entry import Entry, EntryType, Tag
from cairn.schemas.game import GameEntryCreate, GameEntryRead
from cairn.routers.get_tags import _get_or_create_tag


router = APIRouter(prefix="/games", tags=["games"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   \/ POST /games              — log a game session
#   GET  /games              — list (filter: tag, date, status, platform)
#   GET  /games/{id}         — single entry
#
# Models:  cairn/models/game.py     (Game, GameStatus)
# Schemas: cairn/schemas/game.py    (GameEntryCreate, GameEntryRead, GameDetails)

@router.post("/", response_model=GameEntryRead, status_code=201)
def create_game(payload: GameEntryCreate, db: Session = Depends(get_db)):
    entry = Entry(
        type=EntryType.game,
        timestamp=payload.timestamp,
        notes=payload.notes,
    )
    entry.tags = _get_or_create_tag(db, payload.tags)
    entry.game = Game(**payload.game.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/", response_model=list[GameEntryRead])
def list_games(
    tag: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Entry).filter(Entry.type == EntryType.game)
    if tag:
        q = q.join(Entry.tags).filter(Tag.name == tag)
    if from_date:
        q = q.filter(Entry.timestamp >= from_date)
    if to_date:
        q = q.filter(Entry.timestamp <= to_date)
    return q.order_by(Entry.timestamp.desc()).offset(offset).limit(limit).all()

@router.get("/{entry_id}", response_model=GameEntryRead)
def get_game(entry_id: int, db: Session = Depends(get_db)):
    entry = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.type == EntryType.game)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Game not found")
    return entry
