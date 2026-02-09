from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Players
from schemas.player_dto import PlayerBase, PlayerCreate, PlayerGetByNick

class PlayerRepository():
    
    async def get_player(self, player: PlayerBase, session: AsyncSession):
        result = await session.execute(select(Players).where(Players.id==player.id))
        result = result.scalars().first()
        if result != None:
            return result
        return None      
    
    async def get_player_by_nickname(self, player: PlayerGetByNick, session: AsyncSession):
        result = session.execute(select(Players).where(Players.nickname==player.nickname))
        result = result.scalars().first()
        if result != None:
            return result
            
        return None
    
    async def get_all_players(self, session: AsyncSession):
        results = session.execute(select(Players))
        return results.scalars.all()
    
    async def create_player(self, player: PlayerCreate, session: AsyncSession):
        await session.add(player)
        await session.commit()

    async def del_player(self, player: PlayerBase, session: AsyncSession):
        await session.delete(player)
        await session.commit()
        

async def get_player_repository():
    return PlayerRepository()