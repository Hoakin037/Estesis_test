from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from .player_dtos import PlayerBase


class GameBase(BaseModel):
    id: UUID


class GameSetEndedTime(GameBase):
    ended_at: datetime


class GameRoom(GameBase):
    player_1: PlayerBase
    player_2: PlayerBase
    boards: dict[int, list] = Field(default_factory=dict)
    current_player_turn: int = 0
    created_at: datetime
    ended_at: datetime | None = Field(default=None)


class CreateGameRequest(BaseModel):
    player_1: PlayerBase
    player_2: PlayerBase


class ResultsBase(BaseModel):
    game_id: str


class ResultsCreate(ResultsBase):
    winner_id: int
    surrender_id: int
    created_at: datetime
    ended_at: datetime
