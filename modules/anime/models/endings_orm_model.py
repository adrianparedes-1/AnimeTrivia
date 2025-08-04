from datetime import datetime
from db.base_orm_model import Base
from typing import List
from modules.anime.models.junction_tables.anime_endings import anime_endings_table
from sqlalchemy import Integer, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Endings(Base):
    __tablename__ = "endings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300), server_default=None, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    animes: Mapped[List["Anime"]] = relationship(
        "Anime",
        secondary=anime_endings_table,
        back_populates="endings"
    )
