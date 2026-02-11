from pydantic import BaseModel

class PlayerBase(BaseModel):
    id: int

class PlayerCreate(BaseModel):
    nickname: str
    password: str

class PlayerGetByNick(BaseModel):
    nickname: str

class PlayerAuth(PlayerGetByNick):
    password: str