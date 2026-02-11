from fastapi import APIRouter, Depends, HTTPException, status

from schemas import PlayerCreate, PlayerAuth, PlayerBase, PlayerGetByNick
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

    return  {
        "success": True
    }
     
@players.post("/login")
async def login(
    player: PlayerAuth,
    auth_service: AuthService = Depends(get_auth_service),
    player_service: PlayerService = Depends(get_player_service)
):
    if await auth_service.authenticate_player(player) == True:
        player_id = await player_service.get_player_by_nickname(PlayerGetByNick(nickname=player.nickname))

        return {
            "player_id": player_id.id
        }
    
    raise HTTPException(status_code=401, detail="Неверный пароль!")    
        
       
    
   

@players.get("")
async def get_free_players(
    player_service: PlayerService = Depends(get_player_service),
    game_storage: GameStorage=Depends(get_game_storage)
) -> dict:
    free_players = await player_service.get_free_players(game_storage)

    return {"free_players": free_players}

@players.get("/{player_sid}/stats")
async def get_player_stats(
    player_sid: int,
    results_service: ResultsService = Depends(get_results_service)
):
    player = PlayerBase(id=player_sid)
    return await results_service.get_player_results(player)
