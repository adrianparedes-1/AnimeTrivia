from datetime import datetime
from db.base_orm_model import Base
from typing import List
from sqlalchemy import Integer, func, String
from modules.anime.models.junction_tables.anime_studios import anime_studios_table
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Studios(Base):
    __tablename__ = "studios"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())


    animes: Mapped[List["Anime"]] = relationship(
        "Anime",
        secondary=anime_studios_table,
        back_populates="studios"
    )
