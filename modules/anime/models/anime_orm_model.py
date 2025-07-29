from datetime import datetime
from typing import Optional
from db.base_orm_model import Base
from sqlalchemy import Integer, String, Float, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from modules.anime.models.theme_orm_model import Theme
    from modules.anime.models.topical_theme_orm_model import TopicalTheme
    from modules.anime.models.title_orm_model import Title
    from modules.anime.models.genre_orm_model import Genre
    from modules.anime.models.studio_orm_model import Studio
    from modules.anime.models.image_orm_model import Image
    from modules.anime.models.trailer_orm_model import Trailer

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

    topical_themes: Mapped[List["TopicalTheme"]] = relationship(back_populates="anime")
    themes: Mapped[List["Theme"]] = relationship(back_populates="anime")
    trailer: Mapped["Trailer"] = relationship(back_populates="anime")
    titles: Mapped[List["Title"]] = relationship(back_populates="anime")
    genres: Mapped[List["Genre"]] = relationship(back_populates="anime")
    studios: Mapped[List["Studio"]] = relationship(back_populates="anime")
    image: Mapped["Image"] = relationship(back_populates="anime")