from datetime import datetime
from db.base_orm_model import Base
from typing import Optional
from sqlalchemy import Integer, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Opening(Base):
    __tablename__ = "opening"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())


    theme_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('theme.id'), server_default=None)
    theme: Mapped["Theme"] = relationship("Theme", back_populates="openings") 