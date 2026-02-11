from typing import Dict
from schemas import GameRoom, GameBase
from uuid import UUID

class GameStorage:
    def __init__(self):
        self.active_games: Dict[UUID, GameRoom] = {}

    async def add_game(self, room: GameRoom):
        self.active_games[room.id] = room

    async def get_game(self, game: GameBase):
        return self.active_games.get(game.id)

    async def del_game(self, game: GameBase):
        self.active_games.pop(game.id, None)
      
    async def get_all_games(self):
        return list(self.active_games.values())


active_games_storage = GameStorage()

async def get_game_storage():
    return active_games_storage