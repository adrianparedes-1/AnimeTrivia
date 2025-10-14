from dto.base_dto import Base
from typing import Optional, List
from pydantic import RootModel
class Player(Base):
    id: int
    username: str
    display_name: Optional[str] = None
    # score: Optional [int] = 0

class Players(RootModel):
    root: List[Player]