from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, func, ForeignKey, String
from typing import List, Optional
from modules.anime.models.junction_tables.anime_titles import anime_titles_table
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Titles(Base):
    __tablename__ = "titles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[Optional[str]] = mapped_column(String(50), server_default=None)
    name: Mapped[str] = mapped_column(String(300), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    animes: Mapped[List["Anime"]] = relationship(
        "Anime",
        secondary=anime_titles_table,
        back_populates="titles"
    )