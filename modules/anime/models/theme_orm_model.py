from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from modules.anime.models.anime_orm_model import Anime
    from modules.anime.models.opening_orm_model import Opening
    from modules.anime.models.ending_orm_model import Ending


class Theme(Base):
    __tablename__ = "theme"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    anime_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('anime.id'), server_default=None)
    anime: Mapped["Anime"] = relationship("Anime", back_populates="themes")

    openings: Mapped[List["Opening"]] = relationship(back_populates="theme")
    endings: Mapped[List["Ending"]] = relationship(back_populates="theme")