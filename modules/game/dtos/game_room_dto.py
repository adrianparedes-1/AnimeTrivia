from dto.base_dto import Base
from modules.game.dtos.player_dto import Players, Player
from modules.game.dtos.song_dto import Song
from typing import List, Mapping, Optional
from modules.game.dtos.clean_retrieval import AnimeRedis
from pydantic import RootModel

class Scoreboard(Base):
    players_scores: Mapping[int, int]
    rounds: int

class GameRoom(Base):
    timer: Optional[float] = None
    players: Optional[Players] = None
    anime_list: Optional[List[AnimeRedis]] = None
    scoreboard: Optional[Scoreboard] = None


class Guess(Base):
    name: Optional[str] = None
