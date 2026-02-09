from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import GameBase, GameCreate, GameSetEndedTime
from db import get_game_repository, GameRepository
from core.security import get_settings, Settings

class GameService():
    def __init__(self, rep: GameRepository, settings: Settings,session: AsyncSession):
        self.rep = rep
        self.settings = settings
        self.session = session

        
