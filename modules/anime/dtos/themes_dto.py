from dto.base_dto import Base
from typing import List
from dtos.openings_dto import Openings
from dtos.endings_dto import Endings

class Themes(Base):
    openings: List[Openings]
    endings: List[Endings]