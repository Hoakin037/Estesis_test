from pydantic import BaseModel
from uuid import uuid4

class UserBase(BaseModel):
    id: str 

class UserCreate(UserBase):
    nickname: str
    password: str
    in_game: bool

 