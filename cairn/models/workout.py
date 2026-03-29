from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from cairn.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), primary_key=True)
    workout_type = Column(String(64), nullable=False)  # run, lift, yoga, swim, etc.
    duration_min = Column(Integer)
    distance_km = Column(Float)

    entry = relationship("Entry", back_populates="workout")
