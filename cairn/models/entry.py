import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
from cairn.database import Base


class EntryType(str, enum.Enum):
    hike = "hike"
    game = "game"
    media = "media"
    workout = "workout"
    mood = "mood"


entry_tags = Table(
    "entry_tags",
    Base.metadata,
    Column("entry_id", Integer, ForeignKey("entries.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False, index=True)

    entries = relationship("Entry", secondary="entry_tags", back_populates="tags")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(EntryType), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    notes = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    tags = relationship("Tag", secondary="entry_tags", back_populates="entries")

    hike = relationship("Hike", back_populates="entry", uselist=False, cascade="all, delete-orphan")
    game = relationship("Game", back_populates="entry", uselist=False, cascade="all, delete-orphan")
    media = relationship("Media", back_populates="entry", uselist=False, cascade="all, delete-orphan")
    workout = relationship("Workout", back_populates="entry", uselist=False, cascade="all, delete-orphan")
    mood = relationship("Mood", back_populates="entry", uselist=False, cascade="all, delete-orphan")
