from dto.base_dto import Base
from pydantic import Field
from typing import List, Optional
from modules.anime.dtos.themes_dto import ThemesDto
from modules.anime.dtos.trailer_dto import TrailerDto
from modules.anime.dtos.titles_dto import TitlesDto
from modules.anime.dtos.genres_dto import GenresDto
from modules.anime.dtos.studios_dto import StudiosDto
from modules.anime.dtos.images_dto import ImagesDto

class AnimeDto(Base):
    title: str
    mal_id: int
    rank: int
    score: float
    scored_by: int
    popularity: int
    times_favorited: int
    members_MAL: int
    synopsis: str
    release_year: int
    release_season: str
    themes: Optional[List[ThemesDto]] = Field(default=None)
    trailer: TrailerDto
    titles: List[TitlesDto]
    genres: List[GenresDto]
    studios: List[StudiosDto]
    images: List[ImagesDto]