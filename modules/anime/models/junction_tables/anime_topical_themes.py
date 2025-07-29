from sqlalchemy import Table, Column, ForeignKey
from db.base_orm_model import Base

anime_topical_themes_table = Table(
    "anime_topical_themes",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.id"), primary_key=True),
    Column("topical_theme_id", ForeignKey("topical_themes.id"), primary_key=True),
)