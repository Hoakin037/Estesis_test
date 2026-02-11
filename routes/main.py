from fastapi import APIRouter
from .game import games
from .players import players

router = APIRouter()
router.include_router(games)
router.include_router(players)
