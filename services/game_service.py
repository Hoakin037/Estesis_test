from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import GameBase, GameCreate, GameSetEndedTime
from db import get_session
from .game_logics import generate_full_board, shoot


class GameService():
    

