from dto.base_dto import Base
from pydantic import Field
from typing import List, Optional
from modules.anime.dtos.trailer_dto import TrailerDto
from modules.anime.dtos.titles_dto import TitlesDto
from modules.anime.dtos.genres_dto import GenresDto
from modules.anime.dtos.studios_dto import StudiosDto
from modules.anime.dtos.images_dto import ImagesDto
from modules.anime.dtos.topical_themes_dto import TopicalThemesDto

class AnimeDto(Base):
    name: str = Field("title")
    mal_id: int
    rank: Optional[int]
    score: float
    scored_by: int
    popularity: int
    times_favorited: int = Field(alias="favorites")
    members_MAL: int = Field(alias="members")
    synopsis: str
    release_year: Optional[int] = Field(alias="year", default=None)
    release_season: Optional[str] = Field(alias="season", default=None)
    topical_themes: Optional[List[TopicalThemesDto]] = Field(alias="themes", default=None)
    trailer: Optional[TrailerDto]
    titles: List[TitlesDto]
    genres: List[GenresDto]
    studios: List[StudiosDto]
    image: ImagesDto = Field(alias="images")

class Data(Base):
    animes: List[AnimeDto] = Field(alias="data")