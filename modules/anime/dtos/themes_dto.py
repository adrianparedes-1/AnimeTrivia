from dto.base_dto import Base
from typing import List, Optional
from modules.anime.dtos.openings_dto import OpeningsDto
from modules.anime.dtos.endings_dto import EndingsDto

class ThemesDto(Base):
    openings: Optional[List[OpeningsDto]]
    endings: Optional[List[EndingsDto]]