from sqlalchemy import Table, Column, ForeignKey
from db.base_orm_model import Base

anime_genres_table = Table(
    "anime_genres",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)
