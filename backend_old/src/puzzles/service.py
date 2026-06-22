from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .model import Puzzles
from .schema import PuzzleCreate, PuzzleUpdate, PuzzleResponse
from users.model import Users
from .utils import generate_clues, calculate_difficulty
from auth import get_current_user
from fastapi import Depends




async def get_puzzles(db: AsyncSession, min_hor_size=None, min_ver_size=None, difficulty=None, sort_by="created_at", direction="desc", offset: int = 0, limit: int = 100, creator_id: int = None):
    filters = []

    limit = min(limit, 100)
    offset = max(offset, 0)
    order_by = getattr(Puzzles, sort_by)

    if direction == "asc":
        order_by = order_by.asc()
    else:
        order_by = order_by.desc()

    if min_hor_size is not None:
        filters.append(Puzzles.hor_size >= min_hor_size)
    if min_ver_size is not None:
        filters.append(Puzzles.ver_size >= min_ver_size)
    if difficulty:
        filters.append(Puzzles.difficulty == difficulty)

    if creator_id:
        filters.append(Puzzles.author_id == creator_id)
            

    result = await db.execute(select(Puzzles, Users.username.label("author_username"))
                              .outerjoin(Users, Puzzles.author_id == Users.id)
                              .where(*filters).order_by(order_by)
                              .offset(offset).limit(limit))
    rows = result.all()
    return [PuzzleResponse(
        id=p.id,
        title=p.title,
        hor_size=p.hor_size,
        ver_size=p.ver_size,
        difficulty=p.difficulty,
        row_clues=p.row_clues,
        col_clues=p.col_clues,
        solution_grid=p.solution_grid,
        author_username=username
    ) for p, username in rows
]

async def get_puzzles_by_creator(db: AsyncSession, creator_id: int):
    result = await db.execute(select(Puzzles, Users.username.label("author_username"))
                              .outerjoin(Users, Puzzles.author_id == Users.id)
                              .where(Puzzles.author_id == creator_id))
    rows = result.all()
    return [PuzzleResponse(
        id=p.id,
        title=p.title,
        hor_size=p.hor_size,
        ver_size=p.ver_size,
        difficulty=p.difficulty,
        row_clues=p.row_clues,
        col_clues=p.col_clues,
        solution_grid=p.solution_grid,
        author_username=username
    ) for p, username in rows]

async def get_puzzle(db: AsyncSession, puzzle_id: int):
    result = await db.execute(select(Puzzles, Users.username.label("author_username"))
                              .outerjoin(Users, Puzzles.author_id == Users.id)
                              .where(Puzzles.id == puzzle_id))
    row = result.first()
    if not row:
        return None
    p, username = row
    return PuzzleResponse(
        id=p.id,
        title=p.title,
        hor_size=p.hor_size,
        ver_size=p.ver_size,
        difficulty=p.difficulty,
        row_clues=p.row_clues,
        col_clues=p.col_clues,
        solution_grid=p.solution_grid,
        author_username=username
    )

async def get_puzzle_by_creator(db: AsyncSession, puzzle_id: int, creator: dict = Depends(get_current_user)):
    result = await db.execute(select(Puzzles).where(Puzzles.id == puzzle_id, Puzzles.author_id == creator.id))
    return result.scalars().first()

async def create_puzzle(db: AsyncSession, puzzle: PuzzleCreate, current_user: dict = Depends(get_current_user)):
    db_puzzle = Puzzles(**puzzle.model_dump())
    row_clues, col_clues = generate_clues(puzzle.solution_grid)
    db_puzzle.row_clues = row_clues
    db_puzzle.col_clues = col_clues
    db_puzzle.difficulty = calculate_difficulty(puzzle.solution_grid)
    db_puzzle.author_id = current_user.id
    db.add(db_puzzle)
    await db.commit()
    await db.refresh(db_puzzle)
    return db_puzzle

async def update_puzzle(db: AsyncSession, db_puzzle: Puzzles, puzzle: PuzzleUpdate, current_user: dict = Depends(get_current_user)):
    clean_data = puzzle.model_dump(exclude_unset=True)
    if "solution_grid" in clean_data:
        row_clues, col_clues = generate_clues(clean_data["solution_grid"])
        clean_data["row_clues"] = row_clues
        clean_data["col_clues"] = col_clues
        clean_data["difficulty"] = calculate_difficulty(clean_data["solution_grid"])
    for key, value in clean_data.items():
        setattr(db_puzzle, key, value)
    await db.commit()
    await db.refresh(db_puzzle)
    return db_puzzle

async def delete_puzzle(db: AsyncSession, db_puzzle: Puzzles):
    await db.delete(db_puzzle)
    await db.commit()
    return db_puzzle
