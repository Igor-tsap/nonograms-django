from typing import Optional
from jose import JWTError, jwt
from users.model import Users
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from .model import ChatMessage as ChatMessageModel
from .schema import ChatMessageCreate
from database.redis import redis


async def publish_chat_message(room_id: str, message: str):
    await redis.publish(f"puzzle_{room_id}", message)
async def get_username_from_token( db: AsyncSession, token: Optional[str]) -> str:
    if token is None:
        return "Anonymous"
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        print(f"[auth] payload: {payload}")
        user_id = payload.get("id")
        if not user_id:
            return "Anonymous"
        result = await db.execute(select(Users).where(Users.id == user_id))
        user = result.scalars().first()
        return user.username if user else "Anonymous"
    except JWTError:
        return "Anonymous"
    except Exception as e:
        print(f"[get_username_from_token] error: {e}")
        print(f"[ws] error: {e}")
        return "Anonymous"
    
async def get_chat_messages(db: AsyncSession, room_id: int, limit: int = 50, offset: int = 0):
    limit = min(limit, 50)
    
    query = (select(ChatMessageModel)
             .where(ChatMessageModel.room_id == room_id)
             .order_by(desc(ChatMessageModel.created_at))
             .offset(offset)
             .limit(limit)
             )
    result = await db.execute(query)
    messages = result.scalars().all()
    return messages[::-1]

async def create_chat_message(db: AsyncSession, room_id: str, message_data: ChatMessageCreate):
    try:
        room_id_int = int(room_id)
    except ValueError:
        room_id_int = 0
    db_message = ChatMessageModel(room_id=room_id_int, **message_data.model_dump())
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message