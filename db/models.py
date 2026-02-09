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

class Games(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime, default=None)  # если не установлено, то игра активна
    player_1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player_2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))

    player_1 = relationship("Players", back_populates="games_as_player_1", foreign_keys=[player_1_id])
    player_2 = relationship("Players", back_populates="games_as_player_2", foreign_keys=[player_2_id])
    results_created_at = relationship("Results", back_populates="created")
    results_ended_at = relationship("Results", back_populates="ended")


class Results(Base):
    __tablename__ = "results"

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    winner_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    surrender_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    created_at: Mapped[datetime] = mapped_column(ForeignKey("games.created_at")) 
    ended_at: Mapped[datetime] = mapped_column(ForeignKey("games.ended_at")) 

    winner = relationship("Players", back_populates="results_as_winner")
    surrender = relationship("Players", back_populates="results_as_surrender")
    created = relationship("Games", back_populates=("results_created_at"))
    ended = relationship("Games", back_populates=("results_ended_at"))