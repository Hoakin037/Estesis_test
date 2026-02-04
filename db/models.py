from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime, Column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(length=200))
    password: Mapped[str] = mapped_column(String(32), nullable=False)
    in_game: Mapped[bool] = mapped_column(default=False)

    game_as_player_1 = relationship("games", back_populates="player1", foreign_keys="games.player_1_id" )
    game_as_player_2 = relationship("games", back_populates="player2", foreign_keys="games.player_2_id" )
    boards = relationship("boards", back_populates="player")

class Games(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    winner_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    player_1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player_2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    is_active: Mapped[bool] = mapped_column(default=True )

    player_1 = relationship("players", back_populates="games_as_player_1", foreign_keys=[player_1_id])
    player_2 = relationship("players", foreign_keys=[player_2_id])
    boards = relationship("boards", back_populates="game", cascade="all, delete-orphan")

class Boards(Base):
    __tablename__ = "boards"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey(""))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    field: Mapped[list] = mapped_column()

    game = relationship("games", back_populates="boards")
    player = relationship("player", back_populates="boards")
