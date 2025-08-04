from datetime import datetime
from typing import Optional
from db.base_orm_model import Base
from sqlalchemy import Integer, String, Float, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modules.anime.models.junction_tables.anime_studios import anime_studios_table
from modules.anime.models.junction_tables.anime_titles import anime_titles_table
from modules.anime.models.junction_tables.anime_genres import anime_genres_table
from modules.anime.models.junction_tables.anime_topical_themes import anime_topical_themes_table
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from modules.anime.models.theme_orm_model import Themes
    from modules.anime.models.topical_themes_orm_model import TopicalThemes
    from modules.anime.models.titles_orm_model import Titles
    from modules.anime.models.genres_orm_model import Genres
    from modules.anime.models.studios_orm_model import Studios
    from modules.anime.models.image_orm_model import Image
    from modules.anime.models.trailer_orm_model import Trailer

class Anime(Base):
    __tablename__ = "anime"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mal_id: Mapped[int] = mapped_column(Integer, server_default=None)
    name: Mapped[str] = mapped_column(String(300))
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

    topical_themes: Mapped[List["TopicalThemes"]] = relationship(
        secondary=anime_topical_themes_table,
        back_populates="animes",
        single_parent=True,
        cascade="all, delete-orphan",
        passive_deletes=True
        )
    titles: Mapped[List["Titles"]] = relationship(
        secondary=anime_titles_table,
        back_populates="animes",
        single_parent=True,
        cascade="all, delete-orphan",
        passive_deletes=True        
        )
    genres: Mapped[List["Genres"]] = relationship(
        secondary=anime_genres_table,
        back_populates="animes",
        single_parent=True,
        cascade="all, delete-orphan",
        passive_deletes=True        
        )
    studios: Mapped[List["Studios"]] = relationship(
        secondary=anime_studios_table,
        back_populates="animes",
        single_parent=True,
        cascade="all, delete-orphan",
        passive_deletes=True        
        )
    themes: Mapped[List["Themes"]] = relationship(back_populates="anime")
    trailer: Mapped["Trailer"] = relationship(back_populates="anime")
    image: Mapped["Image"] = relationship(back_populates="anime")