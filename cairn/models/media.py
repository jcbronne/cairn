import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from cairn.database import Base


class MediaType(str, enum.Enum):
    book = "book"
    film = "film"
    tv = "tv"
    podcast = "podcast"
    album = "album"


class MediaStatus(str, enum.Enum):
    in_progress = "in_progress"
    finished = "finished"
    dropped = "dropped"


class Media(Base):
    __tablename__ = "media"

    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), primary_key=True)
    title = Column(String(256), nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)
    creator = Column(String(256))  # author, director, artist, etc.
    status = Column(Enum(MediaStatus))
    rating = Column(Integer)  # 1–10

    entry = relationship("Entry", back_populates="media")
