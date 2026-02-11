from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .tables import Players
from schemas.player_dtos import PlayerBase, PlayerCreate, PlayerGetByNickname


class PlayerRepository():

    async def get_player(self, player: PlayerBase, session: AsyncSession):
        result = await session.execute(select(Players).where(Players.id == player.id))
        result = result.scalars().first()

        return result

    async def get_player_by_nickname(self, player: PlayerGetByNickname, session: AsyncSession):
        result = await session.execute(select(Players).where(Players.nickname == player.nickname))
        result = result.scalars().first()

        return result

    async def get_all_players(self, session: AsyncSession):
        results = await session.execute(select(Players))
        return results.scalars().all()

    async def create_player(self, player: PlayerCreate, session: AsyncSession):
        session.add(Players(password=player.password,
                    nickname=player.nickname))
        await session.commit()

    async def delete_player(self, player: PlayerBase, session: AsyncSession):
        await session.delete(player)
        await session.commit()


async def get_player_repository():
    return PlayerRepository()
