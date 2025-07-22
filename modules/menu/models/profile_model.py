from datetime import datetime
from db.base_orm_model import Base
from modules.user.models.user_model import User
from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Dict, Optional
from sqlalchemy import JSON


class Profile(Base):
    __tablename__ = "profile"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    display_name: Mapped[str] = mapped_column(String(50))
    player_history: Mapped[Dict] = mapped_column(JSON, server_default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(server_default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())

    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user.id'), server_default=None)
    user: Mapped["User"] = relationship()