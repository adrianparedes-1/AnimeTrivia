from sqlalchemy import Table, Column, ForeignKey
from db.base_orm_model import Base

anime_studios_table = Table(
    "anime_studios",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
    Column("studio_id", ForeignKey("studios.id", ondelete="CASCADE"), primary_key=True),
)
