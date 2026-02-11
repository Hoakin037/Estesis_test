from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from datetime import datetime
from uuid import UUID as PyUUID 

class Base(DeclarativeBase):
    pass


class Players(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(length=200), unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    results_as_winner = relationship(
        "Results",
        back_populates="winner",
        foreign_keys="[Results.winner_id]"         
    )
    results_as_surrender = relationship(
        "Results",
        back_populates="surrender",
        foreign_keys="[Results.surrender_id]"        
    ) 

 
class Results(Base):
    __tablename__ = "results"

    game_id: Mapped[PyUUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    winner_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    surrender_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    winner = relationship(
        "Players",
        back_populates="results_as_winner",
        foreign_keys=[winner_id]                     
    )
    surrender = relationship(
        "Players",
        back_populates="results_as_surrender",
        foreign_keys=[surrender_id]
    )