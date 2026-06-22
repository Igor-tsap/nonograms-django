from database.core import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone



class Puzzles(Base):
    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    hor_size = Column(Integer, index=True)
    ver_size = Column(Integer, index=True)
    difficulty = Column(String(255), index=True)
    solution_grid = Column(JSON)
    row_clues = Column(JSON)
    col_clues = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    author = relationship("Users", back_populates="puzzles")
    attempts = relationship("Attempts", back_populates="puzzle")
