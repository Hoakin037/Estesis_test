from typing import Dict
from schemas import GameRoom, GameBase, GameSetEndedTime


class GameStorage:
    def __init__(self):
        self.active_games: Dict[str, GameRoom] = {}

    def add_game(self, game: GameRoom):
        self.active_games[game.id] = game

    def get_game(self, game: GameBase):
        return self.active_games.get(game.id)

    def del_game(self, game: GameBase):
        self.active_games.pop(game.id, None)

    def set_game_ended_time(self, game: GameSetEndedTime):
       self.active_games[game.id].ended_at = game.ended_at
       
    def get_all_games(self):
        return list(self.active_games.values())


