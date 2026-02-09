from pydantic import BaseModel, Field
from datetime import datetime

from .player_dto import PlayerInGame

class GameBase(BaseModel):
    id: int

class GameCreate(GameBase):
    player_1_id: int
    player_2_id: int
    created_at: datetime
    ended_at: None

class GameSetEndedTime(GameBase):
    ended_at: datetime
    
class GameRoom(GameBase):
    player_1: PlayerInGame
    player_2: PlayerInGame
    boards: dict[int, list[list[str]]] = Field(default_factory=dict)
    current_player_turn: int = 0

class ResultsBase(BaseModel):
    game_id: int

class ResultsCreate(ResultsBase):
    winner_id: int
    surrender_id: int
    created_at: datetime
    ended_at: datetime