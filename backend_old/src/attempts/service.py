from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .model import Attempts
from .schema import AttemptCreate, AttemptUpdate
from puzzles.model import Puzzles


def normalize(grid):
    return [[1 if cell == 1 else 0 for cell in row] for row in grid]

async def get_attempts(db: AsyncSession,  user_id: int = None):
    result = await db.execute(select(Attempts).where(Attempts.user_id == user_id).order_by(Attempts.created_at.desc()))
    return result.scalars().all()

async def get_attempt(db: AsyncSession, attempt_id: int):
    result = await db.execute(select(Attempts).where(Attempts.id == attempt_id))
    return result.scalars().first()


async def create_attempt(db: AsyncSession, attempt: AttemptCreate, puzzle: Puzzles, user_id: int):
    db_attempt = Attempts(**attempt.model_dump())
    db_attempt.status = "in_progress"
    db_attempt.current_grid = [[0 for _ in range(puzzle.hor_size)] for _ in range(puzzle.ver_size)]
    db_attempt.time_spent = 0
    db_attempt.user_id = user_id
    db_attempt.puzzle_id = puzzle.id
    db.add(db_attempt)
    await db.commit()
    await db.refresh(db_attempt)
    return db_attempt

async def update_attempt(db: AsyncSession, db_attempt: Attempts, attempt: AttemptUpdate, puzzle: Puzzles, user_id: int):
    for key, value in attempt.model_dump(exclude_unset=True).items():
        setattr(db_attempt, key, value)
    if normalize(attempt.current_grid) == normalize(puzzle.solution_grid):
        db_attempt.status = "completed"
        db_attempt.current_grid = [[2 if cell == 0 else cell for cell in row] for row in attempt.current_grid]
    else:
        db_attempt.status = "in_progress"
    await db.commit()
    await db.refresh(db_attempt)
    return db_attempt