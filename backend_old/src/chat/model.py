from database.core import Base
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime, timezone

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, index=True)  # puzzle id
    username = Column(String(255))
    message = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))