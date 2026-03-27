from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from cairn.database import Base


class Mood(Base):
    __tablename__ = "moods"

    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), primary_key=True)
    score = Column(Integer, nullable=False)  # 1–10
    energy = Column(Integer)  # 1–5

    entry = relationship("Entry", back_populates="mood")
