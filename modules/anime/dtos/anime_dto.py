from dto.base_dto import Base
from typing import List
from dtos.themes_dto import Themes
from dtos.trailer_dto import Trailer
from dtos.titles_dto import Titles
from dtos.genres_dto import Genres
from dtos.studios_dto import Studios
from dtos.images_dto import Images

class Anime(Base):
    title: str
    rank: int
    score: float
    scored_by: int
    popularity: int
    times_favorited: int
    members_MAL: int
    synopsis: str
    release_year: int
    release_season: str
    themes: List[Themes]
    trailer: Trailer
    titles: List[Titles]
    genres: List[Genres]
    studios: List[Studios]
    images: List[Images]