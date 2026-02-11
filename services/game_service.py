from fastapi import HTTPException, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import asyncio
from uuid import UUID

from schemas import GameBase, PlayerBase, GameRoom, ResultsCreate
from storage.active_games_storage import GameStorage
from .game_logics import generate_full_board, shoot, check_ships
from storage.active_games_storage import GameStorage
from .results_service import ResultsService
from db import get_session

class GameService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_game(self, game: GameBase, player_1: PlayerBase, player_2: PlayerBase, game_storage: GameStorage):
        board_1, board_2 = generate_full_board(), generate_full_board()
        room = GameRoom(
            id=game.id,
            player_1=player_1,
            player_2=player_2,
            boards= {
                player_1.id: board_1,
                player_2.id: board_2
            },
            current_player_turn=1,
            created_at=datetime.now(timezone.utc)
        )

        await game_storage.add_game(room)
        return room
    
    async def shoot(self, room: GameRoom, player: PlayerBase, game_storage: GameStorage, x: int, y: int, websocket: WebSocket):
        if not (0 <= x < 10 and 0 <= y < 10):
            await websocket.send_json({"type": "error", "message": "Некорректные координаты"})
            return room

        await self.check_current_player_turn(room, player, websocket, x, y)
        game_storage.active_games[room.id] = room # обновление доски после хода

        return room 
    
    async def check_current_player_turn(self, room: GameRoom, player: PlayerBase, websocket: WebSocket, x: int, y: int):
        if room.current_player_turn==1 and player.id==room.player_1.id:
            room.boards[room.player_2.id], room.current_player_turn = await shoot(room.boards[room.player_2.id], websocket, x, y, room.current_player_turn)

        elif room.current_player_turn==2 and player.id==room.player_2.id:
            room.boards[room.player_1.id], room.current_player_turn = await shoot(room.boards[room.player_1.id], websocket, x, y, room.current_player_turn)
        
        else:
            await websocket.send_json({"type": "error", "message": "Сейчас не ваш ход!"})
        
        return

    async def check_game_exist(self, game: GameBase,game_storage=GameStorage):
        result = await game_storage.get_game(game)
        if not result:
            raise HTTPException(status_code=404, detail=f"Игра с id: {game.id} не найдена!")
        
        return result
    
    async def check_player_in_current_game(self, room: GameRoom, player: PlayerBase):
        if room.player_1.id == player.id or room.player_2.id == player.id:
            return True
        return False

    async def wait_for_opponent(self, room: GameRoom, player_id: int, opponent_id: int, websocket: WebSocket):
        if not hasattr(room, "_connected_players"):
            room._connected_players = set()

        room._connected_players.add(player_id)

        if opponent_id not in room._connected_players:
            await websocket.send_json({
                "type": "waiting_for_opponent",
                "message": "Ожидание подключения второго игрока..."
            })

            timeout = 300  # 5 минут ожидания
            start_time = asyncio.get_event_loop().time()

            while opponent_id not in room._connected_players:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Превышено время ожидания подключения оппонента."
                    })
                    raise asyncio.TimeoutError("Время ожидания противника превышено.")

                await asyncio.sleep(0.5)

        await websocket.send_json({
            "type": "game_start",
            "message": "Игра началась!"})

    async def send_play_message(self, room: GameRoom, websocket: WebSocket):
        message = {
            "type": "game_state",
            "player_1": room.player_1.id, 
            "player_2": room.player_2.id,
            "player_1_board": room.boards[room.player_1.id],
            "player_2_board": room.boards[room.player_2.id],
            "current_turn": room.current_player_turn
        }
        await websocket.send_json(message)

    async def send_game_over_message(self, results: ResultsCreate, websocket: WebSocket):
        message = {
            "type": "game_over",
            "winner": results.winner_id, 
            "surrender": results.surrender_id,
            "created_at": results.created_at.isoformat() if results.created_at else None,
            "ended_at": results.ended_at.isoformat() if results.ended_at else None,
        }
        await websocket.send_json(message)

    async def check_game_over(self, room: GameRoom, game_storage: GameStorage, websocket: WebSocket, result_service: ResultsService, player: PlayerBase):

        opponent = room.player_2 if player.id == room.player_1.id else room.player_1
    
        opponent_board = room.boards[opponent.id]
        if not check_ships(opponent_board):  
            results = ResultsCreate(
                game_id=str(room.id),
                winner_id=player.id,
                surrender_id=opponent.id,
                created_at=room.created_at,
                ended_at=datetime.now(timezone.utc)
            )
            await self.send_game_over_message(results, websocket)
            await result_service.create_result(results)
            await game_storage.del_game(GameBase(id=room.id))
            return True  # Игра завершена
            
        return False
    
    async def play(self, room: GameRoom, websocket: WebSocket, player: PlayerBase, game_storage: GameStorage, results_service: ResultsService):
        await self.send_play_message(room, websocket)
        while True:
            client_message = await websocket.receive_json()
            message_type = client_message.get("type")
            
            if message_type == "shoot":
                x, y = client_message.get("x"), client_message.get("y")
                room = await self.shoot(room, player, game_storage, x, y, websocket)
                await self.send_play_message(room, websocket)
                is_game_over = await self.check_game_over(room, game_storage, websocket, results_service, player)
                if is_game_over:

                    return 

    async def check_game_start_conditions(self, game_sid: str, game_storage: GameStorage, websocket: WebSocket, player: PlayerBase, connection_manager):
        room = await self.check_game_exist(GameBase(id=game_sid), game_storage)

        await connection_manager.connect(websocket, game_sid, player.id)
        
        opponent_id = room.player_2.id if player.id == room.player_1.id else room.player_1.id

        # Ждём подключения оппонента
        try:
            await self.wait_for_opponent(room, player.id, opponent_id, websocket)
        except TimeoutError:
            await websocket.close(code=4008, reason="Тайм-аут ожидания оппонента")
            return

        if not await self.check_player_in_current_game(room, player):
            await websocket.close(code=4003, reason="Вы не участник этой игры")
            return
        
        return room

    async def disconnect_players_from_game(self, game_sid: UUID, player: PlayerBase, opponent: PlayerBase, connection_manager):
        current_ws = connection_manager.get_websocket(game_sid, player.id)
        opponent_ws = connection_manager.get_websocket(game_sid, opponent.id)

        if current_ws:
            await current_ws.close(code=1000, reason="Игра завершена")
        if opponent_ws and opponent_ws != current_ws:
            await opponent_ws.close(code=1000, reason="Игра завершена")

        connection_manager.disconnect(current_ws, game_sid, player.id)
        connection_manager.disconnect(opponent_ws, game_sid, opponent.id)

async def get_game_service(session: AsyncSession = Depends(get_session)):
    return GameService(session)



