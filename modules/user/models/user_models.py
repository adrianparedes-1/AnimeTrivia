from db.base_orm_model import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, validates


class UserORM(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    display_name: Mapped[str] = mapped_column(String(50))
    
    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise ValueError("failed email validation by SQLAlchemy")
        return address