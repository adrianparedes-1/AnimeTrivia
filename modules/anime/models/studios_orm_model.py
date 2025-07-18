from datetime import datetime
from db.base_orm_model import Base
from sqlalchemy import Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

class Studios(Base):
    __tablename__ = "studios"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), server_default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())