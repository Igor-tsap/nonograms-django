from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer
from database.core import get_session
from .schema import UserCreate, UserResponse, UserLogin, Token
from . import service

router = APIRouter(prefix="/api/users", tags=["users"])
security = HTTPBearer()

  

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await service.register_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_model=Token)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_session)):
    try:
        result = await service.authenticate_user(db, user.username, user.password)
        if result is None:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        username, is_creator, token = result
        if not token:
            raise HTTPException(status_code=500, detail="Failed to create token")
        return {"name": username, "is_creator": is_creator, "token": token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
