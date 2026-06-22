from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    id: int
    room_id: int
    username: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    username: str
    message: str