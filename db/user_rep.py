from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException

from .models import Player
from schemas.user_dto import UserBase, UserCreate, UserGetByNick

class UserRep():
    
    async def get_user(self, user: UserBase, session: AsyncSession):
        try:
            user = await session.execute(select(Player).where(Player.id==UserBase.id))
            user = user.scalars().first()
            if user:
                return user
            else:
                return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")
    
    async def get_user_by_nickname(self, user: UserGetByNick, session: AsyncSession):
        try:
            user = session.execute(select(Player).where(Player.nickname==UserGetByNick.nickname))
            user = user.scalars().first()
            if user != None:
                return user
            
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")
    async def create_user(self, user: UserCreate, session: AsyncSession):
        await session.add(user)
        await session.commit()

    async def del_user(self, user: UserBase, session: AsyncSession):
        stmt = delete(Player).where(Player.id == user.id)
        await session.execute(stmt)
        await session.commit()

    async def get_in_game_players(self, session: AsyncSession):
        player = select(Player).where(Player.in_game == True)
        result = await session.execute(player)
        return result.scalars().all()

def get_user_rep():
    return UserRep()