from pydantic import BaseModel
from datetime import datetime

class GameBase(BaseModel):
    id: int

class GameCreate(GameBase):
    player_1_id: int
    player_2_id: int
    created_at: datetime
    ended_at: None | datetime = None

