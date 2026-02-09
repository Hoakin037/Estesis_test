from hashlib import sha256
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends

from db import PlayerRepository, get_player_repository
from schemas import PlayerBase, PlayerCreate, PlayerAuth

class AuthService():
    
    def __init__(self, player_rep: PlayerRepository):
        self.player_rep = player_rep
    
    async def authenticate_player(self, player: PlayerAuth):
        exciting_player = self.player_rep.get_player(PlayerBase(id=player.id))
        if exciting_player == None:
            raise HTTPException(status_code=404, detail=f"Пользователь с id: {player.id} не найден!")
        if await self.verify_password(player.password, exciting_player.password) == True:
            return True
        return False
    
    async def hash_password(self, password: str) -> str:
        return sha256(password.encode('utf-8')).hexdigest()

    async def verify_password(self, password: str, hashed_password: str) -> bool:

        password = sha256(password.encode('utf-8')).hexdigest()
        return password == hashed_password
    

async def get_auth_service(player_rep: PlayerRepository = Depends(get_player_repository)):
    return AuthService(player_rep)
