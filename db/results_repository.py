from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .tables import Results
from schemas import ResultsBase, ResultsCreate, PlayerBase
        
class ResultsRepository:    
    async def get_result(self, result: ResultsBase, session: AsyncSession):
        existing_results = await session.execute(select(Results).where(Results.game_id==result.game_id))
        existing_results = existing_results.scalars().first()
        return existing_results

    async def get_all_results(self, session: AsyncSession):
        existing_results = await session.execute(select(Results))
        existing_results = existing_results.scalars().all()
        return existing_results
                     
    async def create_result(self, results: ResultsCreate, session: AsyncSession):
        result = Results(
            game_id=results.game_id,
            winner_id=results.winner_id,
            surrender_id=results.surrender_id,
            created_at = results.created_at,
            ended_at=results.ended_at
        )
        session.add(result)
        await session.commit()
    
    async def get_player_results(self, player: PlayerBase, session: AsyncSession):
        results_win = await session.execute(select(Results).where(Results.winner_id==player.id))
        results_win = results_win.scalars().all()
        results_ser = await session.execute(select(Results).where(Results.surrender_id==player.id))
        results_ser = results_ser.scalars().all()

        return {
            "winner": results_win,
            "serrender": results_ser
        }
    
async def get_results_repository():
    return ResultsRepository()