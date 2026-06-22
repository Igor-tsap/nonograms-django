from pydantic import BaseModel
from typing import List, Optional

class PuzzleCreate(BaseModel):
    title: str
    hor_size: int
    ver_size: int
    solution_grid: List[List[int]]

class PuzzleUpdate(BaseModel):
    title: Optional[str] = None
    hor_size: Optional[int] = None
    ver_size: Optional[int] = None
    solution_grid: Optional[List[List[int]]] = None

class PuzzleResponse(BaseModel):
    id: int
    title: str
    hor_size: int
    ver_size: int
    difficulty: str
    row_clues: List[List[int]]
    col_clues: List[List[int]]
    solution_grid: List[List[int]]
    author_username: Optional[str] = None

    class Config:
        from_attributes = True
