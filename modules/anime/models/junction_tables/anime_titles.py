from sqlalchemy import Table, Column, ForeignKey
from db.base_orm_model import Base

anime_titles_table = Table(
    "anime_titles",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
    Column("title_id", ForeignKey("titles.id", ondelete="CASCADE"), primary_key=True),
)
