from dto.base_dto import Base
from modules.game.dtos.player_dto import Players, Player
from modules.game.dtos.song_dto import Song
from typing import List, Mapping, Optional
from modules.game.dtos.clean_retrieval import AnimeRedis
from pydantic import RootModel


class GameRoom(Base):
    # state: Optional[str] = None
    timer: Optional[float] = None
    players: List[Player]
    anime_list: Optional[List[AnimeRedis]] = None
    scoreboard: Optional[Mapping[str, int]] = None
