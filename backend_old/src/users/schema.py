from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    is_creator: int = 0

class UserResponse(BaseModel):
    id: int
    username: str
    is_creator: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    name: str
    is_creator: int
    token: str
    