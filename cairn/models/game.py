import enum
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from cairn.database import Base


class GameStatus(str, enum.Enum):
    backlog = "backlog"
    playing = "playing"
    completed = "completed"
    dropped = "dropped"


class Game(Base):
    __tablename__ = "games"

    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), primary_key=True)
    title = Column(String(256), nullable=False)
    platform = Column(String(64))
    status = Column(Enum(GameStatus))
    hours = Column(Float)
    rating = Column(Integer)  # 1–10

    entry = relationship("Entry", back_populates="game")
