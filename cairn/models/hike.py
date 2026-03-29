from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from cairn.database import Base


class Hike(Base):
    __tablename__ = "hikes"

    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), primary_key=True)
    trail_name = Column(String(256))
    location = Column(String(256))
    distance_km = Column(Float)
    elevation_gain_m = Column(Float)
    duration_min = Column(Integer)

    entry = relationship("Entry", back_populates="hike")
