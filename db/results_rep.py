from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException

from .models import Results
from schemas import ResultsBase, ResultsCreate
        
class ResultsRepository():    
    async def get_result(self, result: ResultsBase, session: AsyncSession):
        exicting_results = session.execute(select(Results).where(Results.game_id==result.game_id))
        exicting_results = exicting_results.scalars().first()
        return exicting_results

    async def get_all_results(self, session: AsyncSession):
        exicting_results = session.execute(select(Results))
        exicting_results = exicting_results.scalars().all()
        return exicting_results
                     

    async def create_results(self, results: ResultsCreate, session: AsyncSession):
        session.add(results)
        session.commit()

async def get_results_repository():
    return ResultsRepository()