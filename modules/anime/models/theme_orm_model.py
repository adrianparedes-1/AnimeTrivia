from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, func, ForeignKey
# from modules.anime.models.opening_orm_model import Opening
# from modules.anime.models.ending_orm_model import Ending
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class Theme(Base):
    __tablename__ = "theme"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # openings_id: Mapped[int] = mapped_column(Integer, ForeignKey("openings.id"), server_default=None)
    # endings_id: Mapped[int] = mapped_column(Integer, ForeignKey("endings.id"), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    # openings: Mapped[List["Opening"]] = relationship()
    # endings: Mapped[List["Ending"]] = relationship()