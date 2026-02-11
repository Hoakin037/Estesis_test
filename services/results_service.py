from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from db import ResultsRepository, get_results_repository, get_session
from schemas import ResultsBase, ResultsCreate, PlayerBase


class ResultsService:
    def __init__(
            self,
            session: AsyncSession,
            rep: ResultsRepository
    ):
        self.session = session
        self.rep = rep

    async def get_result(self, result: ResultsBase):
        return await self.rep.get_result(result, self.session)

    async def get_all_results(self):
        results = await self.rep.get_all_results(self.session)
        return {
            "results": results
        }

    async def create_result(self, result: ResultsCreate):
        await self.rep.create_result(result, self.session)

    async def get_player_results(self, player: PlayerBase):
        results = await self.rep.get_player_results(player, self.session)
        if results != {
            "winner": [],
            "serrender": []
        }:
            return results
        raise HTTPException(
            status_code=404, detail="У игрока еще нет законченных игр!")


async def get_results_service(
    rep: ResultsRepository = Depends(get_results_repository),
    session: AsyncSession = Depends(get_session)
):
    return ResultsService(session, rep)
