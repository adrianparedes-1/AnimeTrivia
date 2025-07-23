from dto.base_dto import Base
from typing import List
from modules.anime.dtos.openings_dto import OpeningsDto
from modules.anime.dtos.endings_dto import EndingsDto

class ThemesDto(Base):
    openings: List[OpeningsDto]
    endings: List[EndingsDto]