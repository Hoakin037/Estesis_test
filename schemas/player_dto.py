from pydantic import BaseModel
from fastapi import WebSocket

class PlayerBase(BaseModel):
    id: str 

class PlayerCreate(PlayerBase):
    nickname: str
    password: str

class PlayerGetByNick(PlayerBase):
    nickname: str

class PlayerInGame(PlayerBase):
    nickname: str
    websocket: WebSocket