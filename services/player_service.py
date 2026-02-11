from db import get_player_repository, get_session, PlayerRepository
from schemas import PlayerBase, PlayerCreate, PlayerGetByNick
from services import AuthService
from storage.active_games_storage import GameStorage

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends

class PlayerService:
    def __init__(self, rep: PlayerRepository, session: AsyncSession):
        self.rep = rep
        self.session = session

    async def get_player(self, player: PlayerBase):
        result = await self.rep.get_player(player, self.session)
        if result != None:
            return result
        else:
            raise HTTPException(status_code=401, detail="Пользователь не найден!")
    
    async def get_player_by_nickname(self, player: PlayerGetByNick):
        return await self.rep.get_player_by_nickname(PlayerGetByNick(nickname=player.nickname), self.session)
    
    async def add_player(self, player: PlayerCreate, auth_service: AuthService):
        if await self.get_player_by_nickname(PlayerGetByNick(nickname=player.nickname)) != None:
            raise HTTPException(status_code=409, detail="Пользователь с таким никнеймом уже существует!")
        player.password = await auth_service.hash_password(player.password)

        await self.rep.create_player(player, self.session)
       
    async def del_player(self, player: PlayerBase):
        await self.rep.del_player(player, self.session)

    async def get_all_players(self):
        results = await self.rep.get_all_players(self.session)
        if results == []:
            raise HTTPException(status_code=404, detail="Еще нет зарегестрированных игроков.")
        return results
        
    async def get_free_players(self, game_storage: GameStorage):
        all_players = await self.get_all_players()
        busy_player_ids = set()

        for game in game_storage.active_games.values():
            busy_player_ids.add(game.player_1.id)
            busy_player_ids.add(game.player_2.id)

        free_players = [
            {
                "id": p.id,
                "nickname": p.nickname,
            }
            for p in all_players
            if p.id not in busy_player_ids
        ]

        return free_players
        
async def get_player_service(
    rep: PlayerRepository = Depends(get_player_repository),
    session: AsyncSession = Depends(get_session)
):
    return PlayerService(rep, session)