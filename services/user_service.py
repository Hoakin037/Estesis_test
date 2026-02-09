from db import Player, get_user_rep, get_session
from schemas.player_dto import UserBase, UserCreate, UserGetByNick

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

class UserService():
    def __init__(self):
        self.rep = get_user_rep()

    async def get_user(self, user: UserBase):
        try:
            user = await self.rep.get_user(user, self.session)
            if user:
                return user
            else:
                raise HTTPException(status_code=401, detail="Пользователь не найден!")
        except Exception as e:
            raise e

    async def add_user(self, user: UserCreate):
        try:
            if await self.rep.get_user_by_nickname(UserGetByNick(id=user.id, nickname=user.nickname)) != None:
                raise HTTPException(status_code=409, detail="Пользователь с таким никнеймом уже существует!")
            await self.rep.create_user(user)
        except Exception as e:
            raise e
        
    async def del_user(self, user: UserBase):
        await self.del_user(user)