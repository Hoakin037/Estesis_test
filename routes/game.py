from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, WebSocket, Query, WebSocketDisconnect, HTTPException
from asyncio import TimeoutError

from storage.active_games_storage import get_game_storage, GameStorage
from schemas import CreateGameRequest, GameBase, PlayerBase
from services import get_game_service, GameService, ResultsService, get_results_service, PlayerService, get_player_service
from sockets.connect_manager import ConnectionManager

connection_manager = ConnectionManager()
games = APIRouter(prefix="/games")

@games.get("")
async def get_active_games(
    game_storage: GameStorage=Depends(get_game_storage)
    ):
    active_games = await game_storage.get_all_games()
    return {
        "active_games": active_games
    }

@games.post("/create")
async def create_game(
    request: CreateGameRequest,
    player_service: PlayerService = Depends(get_player_service),
    game_service: GameService = Depends(get_game_service),
    game_storage: GameStorage=Depends(get_game_storage)
    ):
    game = GameBase(id=uuid4())
    if await player_service.get_player(request.player_1)==None or await player_service.get_player(request.player_1)==None:
        raise HTTPException(status_code=401, detail="Пользователи не найдены!")
    
    room = await game_service.create_room(game, request.player_1, request.player_2)
    room = await game_service.create_game(room, game_storage)
    return {
        "game_sid": room.id,
        "player_1_id": room.player_1.id,
        "player_2_id": room.player_2.id,
        "player_1_board": room.boards[request.player_1.id],
        "player_2_board": room.boards[request.player_2.id]
    }
 
@games.websocket("/{game_sid}/play")
async def game_play_ws(
    websocket: WebSocket,
    game_sid: UUID,
    player_id: int = Query(..., alias="player_id"),  
    game_service: GameService = Depends(get_game_service),
    game_storage: GameStorage=Depends(get_game_storage),
    results_service: ResultsService = Depends(get_results_service)
) -> None:
    
    player = PlayerBase(id=player_id)
    room = await game_service.check_game_start_conditions(game_sid, game_storage, websocket, player, connection_manager)

    # Если все игроки подключены, то начинаем игру
    try: 
        await game_service.play(room, websocket, player, game_storage, results_service)
        await websocket.close(code=1000, reason="Игра завершена")

    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket, game_sid)
        await connection_manager.broadcast(game_sid, {
            "type": "player_disconnected",
            "player_id": player_id
        }) 

    
        