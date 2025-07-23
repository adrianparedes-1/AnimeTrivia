from datetime import datetime
from db.base_orm_model import Base
from modules.anime.models.anime_orm_model import Anime
from sqlalchemy import Integer, func, ForeignKey, String
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modules.anime.models.anime_orm_model import Anime

class Title(Base):
    __tablename__ = "title"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50), server_default=None)
    title: Mapped[str] = mapped_column(String(300), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    anime_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('anime.id'), server_default=None)
    anime: Mapped["Anime"] = relationship()