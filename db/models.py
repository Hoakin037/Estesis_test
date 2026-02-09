from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, ForeignKey, DateTime, Column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Players(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(length=200), unique=True)
    password: Mapped[str] = mapped_column(String(32), nullable=False)


    game_as_player_1 = relationship("Games", back_populates="player_1", foreign_keys="[games.player_1_id]" )
    game_as_player_2 = relationship("Games", back_populates="player_2", foreign_keys="[games.player_2_id]" )
    results_as_winner = relationship("Results", back_populates="winner")
    results_as_surrender = relationship("Results", back_populates="surrender")

class Results(Base):
    __tablename__ = "results"

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    winner_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    surrender_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(default=None) 

    winner = relationship("Players", back_populates="results_as_winner")
    surrender = relationship("Players", back_populates="results_as_surrender")
    