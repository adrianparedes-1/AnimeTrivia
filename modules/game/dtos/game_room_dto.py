from dto.base_dto import Base
from modules.game.dtos.player_dto import Player
from modules.game.dtos.song_dto import Song
from typing import List, Mapping


class GameRoom(Base):
    state: str
    timer: float
    players: List[Player]
    songs: List[Song]
    scoreboard: Mapping[str, int]
    current_index: int
