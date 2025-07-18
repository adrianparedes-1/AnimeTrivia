from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, String, Float, Text, func
from sqlalchemy.orm import Mapped, mapped_column

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