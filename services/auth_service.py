from hashlib import sha256
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import PlayerRepository, get_player_repository, get_session
from schemas import PlayerAuth, PlayerGetByNickname


class AuthService:

    def __init__(self, player_rep: PlayerRepository, session: AsyncSession):
        self.player_rep = player_rep
        self.session = session

    async def authenticate_player(self, player: PlayerAuth):
        exciting_player = await self.player_rep.get_player_by_nickname(PlayerGetByNickname(nickname=player.nickname), self.session)
        if exciting_player == None:
            raise HTTPException(
                status_code=404, detail=f"Пользователь с id: {player.id} не найден!")
        verification = await self.verify_password(player.password, exciting_player.password)

        return verification

    async def hash_password(self, password: str) -> str:
        return sha256(password.encode('utf-8')).hexdigest()

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        password = sha256(password.encode('utf-8')).hexdigest()
        return password == hashed_password


async def get_auth_service(player_rep: PlayerRepository = Depends(get_player_repository), session: AsyncSession = Depends(get_session)):
    return AuthService(player_rep, session)
