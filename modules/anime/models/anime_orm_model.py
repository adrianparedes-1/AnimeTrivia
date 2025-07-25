from datetime import datetime
from typing import Optional
from db.base_orm_model import Base
from sqlalchemy import Integer, String, Float, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from modules.anime.models import (
    genre_orm_model,
    image_orm_model,
    studio_orm_model,
    theme_orm_model,
    title_orm_model,
    topical_theme_orm_model,
    trailer_orm_model
)

class Anime(Base):
    __tablename__ = "anime"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mal_id: Mapped[int] = mapped_column(Integer, server_default=None)
    title: Mapped[str] = mapped_column(String(300))
    rank: Mapped[Optional[int]] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Float)
    scored_by: Mapped[int] = mapped_column(Integer)
    popularity: Mapped[int] = mapped_column(Integer)
    times_favorited: Mapped[int] = mapped_column(Integer)
    members_MAL: Mapped[int] = mapped_column(Integer)
    synopsis: Mapped[str] = mapped_column(Text)
    release_year: Mapped[Optional[int]] = mapped_column(Integer, server_default=None)
    release_season: Mapped[Optional[str]] = mapped_column(String(50), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    # topical_theme_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('topical_theme.id'), server_default=None)
    topical_theme: Mapped[List["topical_theme_orm_model.TopicalTheme"]] = relationship(back_populates="anime")

    # # theme_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('themes.id'), server_default=None)
    theme: Mapped[List["theme_orm_model.Theme"]] = relationship(back_populates="anime")

    # # trailer_id: Mapped[int] = mapped_column(Integer, ForeignKey('trailer.id'), server_default=None)
    trailer: Mapped["trailer_orm_model.Trailer"] = relationship(back_populates="anime")
    
    # # titles_id: Mapped[int] = mapped_column(Integer, ForeignKey("titles.id"), server_default=None)
    title: Mapped[List["title_orm_model.Title"]] = relationship(back_populates="anime")

    # # genres_id: Mapped[int] = mapped_column(Integer, ForeignKey("genres.id"), server_default=None)
    genre: Mapped[List["genre_orm_model.Genre"]] = relationship(back_populates="anime")

    # # studios_id: Mapped[int] = mapped_column(Integer, ForeignKey("studios.id"), server_default=None)
    studio: Mapped[List["studio_orm_model.Studio"]] = relationship(back_populates="anime")

    # # images_id: Mapped[int] = mapped_column(Integer, ForeignKey("images.id"), server_default=None)
    image: Mapped[List["image_orm_model.Image"]] = relationship(back_populates="anime")