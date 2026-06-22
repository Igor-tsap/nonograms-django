from database.core import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone



class Attempts(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    puzzle_id = Column(Integer, ForeignKey("puzzles.id"))
    status = Column(String(50), default="in_progress")
    current_grid = Column(JSON)
    time_spent = Column(Integer, default=0)  # in seconds
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("Users", back_populates="attempts")
    puzzle = relationship("Puzzles", back_populates="attempts")

