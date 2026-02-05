from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from .models import Player
from schemas.user_dto import UserBase, UserCreate

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

    async def create_user(self, user: UserCreate, session: AsyncSession):
        await session.add(user)
        await session.commit()
        await session.refresh(user)

    async def get_in_game_players(self, session: AsyncSession):
        return await session.execute(select(Player).where(Player.in_game==True))
