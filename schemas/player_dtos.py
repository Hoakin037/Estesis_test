from pydantic import BaseModel


class PlayerBase(BaseModel):
    id: int


class PlayerCreate(BaseModel):
    nickname: str
    password: str


class PlayerGetByNickname(BaseModel):
    nickname: str


class PlayerAuth(PlayerGetByNickname):
    password: str
