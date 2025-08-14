from dto.base_dto import Base
from modules.game.dtos.player_dto import Player
from modules.game.dtos.song_dto import Song
from typing import List, Mapping, Optional


class GameRoom(Base):
    state: Optional[str]
    timer: Optional[float]
    players: Optional[List[Player]]
    songs: Optional[List[Song]]
    scoreboard: Optional[Mapping[str, int]]
    current_index: Optional[int]
