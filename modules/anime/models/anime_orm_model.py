from datetime import datetime
from typing import Optional
from db.base_orm_model import Base
from sqlalchemy import Integer, String, Float, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modules.anime.models import (
    genre_orm_model,
    image_orm_model,
    studio_orm_model,
    theme_orm_model,
    title_orm_model,
    topical_theme_orm_model,
    trailer_orm_model
)
from typing import List

class Anime(Base):
    __tablename__ = "anime"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mal_id: Mapped[int] = mapped_column(Integer, server_default=None)
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

    # topical_theme_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('topical_themes.id'), server_default=None)
    # topical_themes: Mapped[List["topical_theme_orm_model.TopicalThemes"]] = relationship()

    # theme_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('themes.id'), server_default=None)
    # musical_themes: Mapped[List["theme_orm_model.Themes"]] = relationship()

    # trailer_id: Mapped[int] = mapped_column(Integer, ForeignKey('trailer.id'), server_default=None)
    # trailer: Mapped["trailer_orm_model.Trailer"] = relationship()
    
    # titles_id: Mapped[int] = mapped_column(Integer, ForeignKey("titles.id"), server_default=None)
    # titles: Mapped[List["title_orm_model.Titles"]] = relationship()

    # genres_id: Mapped[int] = mapped_column(Integer, ForeignKey("genres.id"), server_default=None)
    # genres: Mapped[List["genre_orm_model.Genres"]] = relationship()

    # studios_id: Mapped[int] = mapped_column(Integer, ForeignKey("studios.id"), server_default=None)
    # studios: Mapped[List["studio_orm_model.Studios"]] = relationship()

    # images_id: Mapped[int] = mapped_column(Integer, ForeignKey("images.id"), server_default=None)
    # images: Mapped[List["image_orm_model.Images"]] = relationship()