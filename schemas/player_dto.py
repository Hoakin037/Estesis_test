from pydantic import BaseModel

class PlayerBase(BaseModel):
    id: str 

class PlayerCreate(PlayerBase):
    nickname: str
    password: str

class PlayerGetByNick(PlayerBase):
    nickname: str
 