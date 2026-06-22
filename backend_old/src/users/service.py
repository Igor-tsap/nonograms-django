from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .model import Users
from .schema import UserCreate
from passlib.context import CryptContext
from dotenv import load_dotenv
from pathlib import Path
from jose import jwt
import os

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

print("SECRET_KEY:", SECRET_KEY)
print("ALGORITHM:", ALGORITHM)

async def register_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = Users(username=user.username, password=hashed_password, is_creator=user.is_creator)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_token(user: Users):
    payload = {"id": user.id, "is_creator": user.is_creator}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(Users).where(Users.username == username))
    user = result.scalars().first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    token = await create_token(user)
    return user.username, user.is_creator, token

