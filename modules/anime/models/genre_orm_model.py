from datetime import datetime
from db.base_orm_model import Base
from typing import Optional
from sqlalchemy import Integer, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Genre(Base):
    __tablename__ = "genre"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre: Mapped[str] = mapped_column(String(50), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    anime_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('anime.id'), server_default=None)
    anime: Mapped["Anime"] = relationship("Anime", back_populates="genres")
