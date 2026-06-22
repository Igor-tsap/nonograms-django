from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.core import get_session
from . import service
from puzzles.service import get_puzzle
from .schema import AttemptCreate, AttemptUpdate, AttemptResponse
from auth import get_current_user

router = APIRouter(prefix="/api/attempts", tags=["attempts"])

@router.get("/", response_model=list[AttemptResponse])
async def read_attempts(db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    attempts = await service.get_attempts(db, current_user.id)
    return attempts

@router.get("/{attempt_id}", response_model=AttemptResponse)
async def read_attempt(attempt_id: int, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    try:
        attempt = await service.get_attempt(db, attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
        if attempt.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to view this attempt")
        return attempt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=AttemptResponse, status_code=201)
async def create_attempt(attempt: AttemptCreate, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    try:
        puzzle = await get_puzzle(db, attempt.puzzle_id)
        if not puzzle:
            raise HTTPException(status_code=404, detail="Puzzle not found")
        return await service.create_attempt(db, attempt, puzzle, current_user.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{attempt_id}", response_model=AttemptResponse)
async def update_attempt(attempt_id: int, attempt: AttemptUpdate, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    try:
        db_attempt = await service.get_attempt(db, attempt_id)
        if not db_attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
        if db_attempt.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to update this attempt")
        puzzle = await get_puzzle(db, db_attempt.puzzle_id)
        updated_attempt = await service.update_attempt(db, db_attempt, attempt, puzzle, current_user.id)
        return updated_attempt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


