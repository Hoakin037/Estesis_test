from fastapi import APIRouter, Depends, HTTPException, status

from schemas import PlayerCreate, PlayerAuth
from services import get_player_service, PlayerService, AuthService, get_auth_service

auth = APIRouter(prefix="/players")

@auth.post('/register', status_code=status.HTTP_201_CREATED)
def register_player(
    player: PlayerCreate,
    player_service: PlayerService = Depends(get_player_service)
):
    player_service.add_player(player)

    return {
        "success": True
    }

@auth.post("/login")
def login(
    player: PlayerAuth,
    auth_service: AuthService = Depends(get_auth_service)
):
    if auth_service.authenticate_player(player) == True:
        return  {
        "success": True
    }
    
    raise HTTPException(status_code=401, detail="Неверный пароль!")