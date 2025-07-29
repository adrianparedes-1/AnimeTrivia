from datetime import datetime
from db.base_orm_model import Base
from typing import List
from modules.anime.models.junction_tables.anime_genres import anime_genres_table
from sqlalchemy import Integer, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Genres(Base):
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre: Mapped[str] = mapped_column(String(50), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    animes: Mapped[List["Anime"]] = relationship(
        "Anime",
        secondary=anime_genres_table,
        back_populates="genres"
    )
