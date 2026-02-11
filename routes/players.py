from fastapi import APIRouter, Depends, HTTPException, status

from schemas import PlayerCreate, PlayerAuth, PlayerBase, PlayerGetByNickname
from services import get_player_service, PlayerService, AuthService, get_auth_service, ResultsService, get_results_service
from storage.active_games_storage import get_game_storage, GameStorage

players = APIRouter(prefix="/players")


@players.post('/register', status_code=status.HTTP_201_CREATED)
async def register_player(
    player: PlayerCreate,
    auth_service: AuthService = Depends(get_auth_service),
    player_service: PlayerService = Depends(get_player_service)
):
    await player_service.add_player(player, auth_service)

    return {
        "nickname": player.nickname
    }


@players.post("/login")
async def login(
    player: PlayerAuth,
    auth_service: AuthService = Depends(get_auth_service),
    player_service: PlayerService = Depends(get_player_service)
):
    authentication = await auth_service.authenticate_player(player)
    if not authentication:
        raise HTTPException(status_code=401, detail="Неверный пароль!")

    player = await player_service.get_player_by_nickname(PlayerGetByNickname(nickname=player.nickname))

    return {
        "player_id": player.id
    }


@players.get("")
async def get_inactive_players(
    player_service: PlayerService = Depends(get_player_service),
    game_storage: GameStorage = Depends(get_game_storage)
):
    inactive_players = await player_service.get_inactive_players(game_storage)

    return {"inactive_players": inactive_players}


@players.get("/{player_sid}/stats")
async def get_player_stats(
    player_sid: int,
    results_service: ResultsService = Depends(get_results_service)
):
    player = PlayerBase(id=player_sid)
    return await results_service.get_player_results(player)
