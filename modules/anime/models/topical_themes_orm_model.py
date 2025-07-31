from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, func, ForeignKey, String
from modules.anime.models.junction_tables.anime_topical_themes import anime_topical_themes_table
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TopicalThemes(Base):
    __tablename__ = "topical_themes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), server_default=None, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    animes: Mapped[List["Anime"]] = relationship(
        "Anime",
        secondary=anime_topical_themes_table,
        back_populates="topical_themes"
    )