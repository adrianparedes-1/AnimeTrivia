from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, String, Float, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modules.anime.models import (
    trailer_orm_model,
    themes_orm_model,
    titles_orm_model,
    genres_orm_model,
    studios_orm_model,
    images_orm_model
)
from typing import List

class Anime(Base):
    __tablename__ = "anime"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    rank: Mapped[int] = mapped_column(Integer, unique=True)
    score: Mapped[float] = mapped_column(Float)
    scored_by: Mapped[int] = mapped_column(Integer)
    popularity: Mapped[int] = mapped_column(Integer)
    times_favorited: Mapped[int] = mapped_column(Integer)
    members_MAL: Mapped[int] = mapped_column(Integer)
    synopsis: Mapped[str] = mapped_column(Text)
    release_year: Mapped[int] = mapped_column(Integer)
    release_season: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    theme_id: Mapped[int] = mapped_column(Integer, ForeignKey('themes.id'), server_default=None)
    themes: Mapped[List["themes_orm_model.Themes"]] = relationship()

    trailer_id: Mapped[int] = mapped_column(Integer, ForeignKey('trailer.id'), server_default=None)
    trailer: Mapped["trailer_orm_model.Trailer"] = relationship()
    
    titles_id: Mapped[int] = mapped_column(Integer, ForeignKey("titles.id"), server_default=None)
    titles: Mapped[List["titles_orm_model.Titles"]] = relationship()

    genres_id: Mapped[int] = mapped_column(Integer, ForeignKey("genres.id"), server_default=None)
    genres: Mapped[List["genres_orm_model.Genres"]] = relationship()

    studios_id: Mapped[int] = mapped_column(Integer, ForeignKey("studios.id"), server_default=None)
    studios: Mapped[List["studios_orm_model.Studios"]] = relationship()

    images_id: Mapped[int] = mapped_column(Integer, ForeignKey("images.id"), server_default=None)
    images: Mapped[List["images_orm_model.Images"]] = relationship()