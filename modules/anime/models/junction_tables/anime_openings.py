from sqlalchemy import Table, Column, ForeignKey
from db.base_orm_model import Base

anime_openings_table = Table(
    "anime_openings",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
    Column("openings_id", ForeignKey("openings.id", ondelete="CASCADE"), primary_key=True),
)