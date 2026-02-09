from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_
from fastapi import HTTPException

from .models import Players, Games
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
    
    async def create_player(self, player: PlayerCreate, session: AsyncSession):
        await session.add(player)
        await session.commit()

    async def del_player(self, player: PlayerBase, session: AsyncSession):
        await session.delete(player)
        await session.commit()
        
    async def get_in_game_players(self, session: AsyncSession):
        result = (
            select(Players)
            .join(Games, or_(
                Games.player_1_id == Players.id,
                Games.player_2_id == Players.id
            ))
            .where(Games.ended_at.is_(None))
            .distinct()
        )
    
        result = await session.execute(result)
        return result.scalars().all()

async def get_player_repository():
    return PlayerRepository()