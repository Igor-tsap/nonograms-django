from database.core import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_creator = Column(Integer, default=0)


    puzzles = relationship("Puzzles", back_populates="author")
    attempts = relationship("Attempts", back_populates="user")