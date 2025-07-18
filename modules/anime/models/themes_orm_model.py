from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, func, ForeignKey
from modules.anime.models.openings_orm_model import Openings
from modules.anime.models.endings_orm_model import Endings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class Themes(Base):
    __tablename__ = "themes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    openings_id: Mapped[int] = mapped_column(Integer, ForeignKey("openings.id"), server_default=None)
    endings_id: Mapped[int] = mapped_column(Integer, ForeignKey("endings.id"), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    openings: Mapped[List["Openings"]] = relationship()
    endings: Mapped[List["Endings"]] = relationship()