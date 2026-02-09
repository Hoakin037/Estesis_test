from db import get_player_repository, get_session, PlayerRepository
from schemas import PlayerBase, PlayerCreate, PlayerGetByNick

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends

class PlayerService():
    def __init__(self, rep: PlayerRepository, session: AsyncSession):
        self.rep = rep
        self.session = session

    async def get_player(self, player: PlayerBase):
        result = await self.rep.get_player(player, self.session)
        if result != None:
            return result
        else:
            raise HTTPException(status_code=401, detail="Пользователь не найден!")
    

    async def add_player(self, player: PlayerCreate):
        if await self.rep.get_player_by_nickname(PlayerGetByNick(id=player.id, nickname=player.nickname), self.session) != None:
            raise HTTPException(status_code=409, detail="Пользователь с таким никнеймом уже существует!")
        await self.rep.create_player(player, self.session)
       
    async def del_player(self, player: PlayerBase):
        await self.rep.del_player(player, self.session)

async def get_player_service(
    rep: PlayerRepository = Depends(get_player_repository),
    session: AsyncSession = Depends(get_session)
):
    return PlayerService(rep, session)