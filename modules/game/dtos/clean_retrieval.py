from dto.base_dto import Base
from modules.game.dtos.title_dto import Title
from modules.game.dtos.song_dto import Song
from typing import List, Mapping, Optional
from pydantic.root_model import RootModel
from pydantic import Field

class CleanList(Base):
    anime: Optional[str] = Field(alias="name", default=None)
    openings: Optional[List[Song]] = []
    endings: Optional[List[Song]] = []
    titles: Optional[List[Title]] = []
