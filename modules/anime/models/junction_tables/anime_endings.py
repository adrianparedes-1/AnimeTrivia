from sqlalchemy import Table, Column, ForeignKey
from db.base_orm_model import Base

anime_endings_table = Table(
    "anime_endings",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
    Column("endings_id", ForeignKey("endings.id", ondelete="CASCADE"), primary_key=True),
)