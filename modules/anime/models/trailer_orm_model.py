from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, String, func, URL
from sqlalchemy.orm import Mapped, mapped_column

class Trailer(Base):
    __tablename__ = "trailer"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(100), server_default=None)
    embed_url: Mapped[str] = mapped_column(String(100), server_default=None)
    youtube_id: Mapped[str] = mapped_column(String(100), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())