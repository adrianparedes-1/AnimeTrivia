from dto.base_dto import Base
from typing import List, Optional
from pydantic import Field

class ThemesDto(Base):
    openings: Optional[List[str]]
    endings: Optional[List[str]]


class Data(Base):
    data: Optional[ThemesDto] = Field(default=None)