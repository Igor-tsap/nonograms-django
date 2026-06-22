from pydantic import BaseModel


class AttemptCreate(BaseModel):
    puzzle_id: int

class AttemptUpdate(BaseModel):
    current_grid: list[list[int]]

class AttemptResponse(BaseModel):
    id: int
    user_id: int
    puzzle_id: int
    status: str
    current_grid: list[list[int]]
    time_spent: int

    class Config:
        from_attributes = True
