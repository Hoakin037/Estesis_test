from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException

from .models import Players, Games, Results
from schemas import GameBase, GameCreate, ResultsBase, ResultsCreate, GameSetEndedTime

class GameRepository():
    async def get_game(self, game: GameBase, session: AsyncSession):
        result = await session.execute(select(Games).where(Games.id==game.id))
        result = result.scalars().first()
        if result != None:
            return result
        return None
        
    async def get_active_games(self, session: AsyncSession):
        results = await session.execute(select(Games).where(Games.ended_at==None))
        results = results.scalars().all()
        if results != None:
            return results
        return None
        
    async def create_game(self, game: GameCreate, session: AsyncSession):
        await session.add(game)
        await session.commit()
        
    async def set_game_ended_time(self, game: GameSetEndedTime, session: AsyncSession):
        exicting_game = self.get_game(GameBase(id=game.id), session)
        exicting_game.ended_at = game.ended_at
        await session.commit()
        await session.refresh(exicting_game)

    async def del_game(self, game: GameBase, session: AsyncSession):
        await session.delete(game)
        await session.commit()
        
        
class ResultsRepository():    
    async def get_result(self, result: ResultsBase, session: AsyncSession):
        exicting_results = session.execute(select(Results).where(Results.game_id==result.game_id))
        exicting_results = exicting_results.scalars().first()
        if exicting_results != None:
            return exicting_results
        return None

    async def get_all_results(self, session: AsyncSession):
        try:
            exicting_results = session.execute(select(Results))
            exicting_results = exicting_results.scalars().all()
            if exicting_results != None:
                return exicting_results
            raise HTTPException(status_code=404, detail="Еще нет завершенных игр.")
        except HTTPException:
            raise                              
