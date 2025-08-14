from db.session_manager import get_db
from sqlalchemy.orm import joinedload, load_only
from modules.game.dtos.game_room_dto import GameRoom
from modules.game.dtos.clean_retrieval import CleanList
from modules.anime.models.anime_orm_model import Anime
from dependencies.redis_client import get_client
import json

'''
create a game room obj using the Game Room DTO.
We will query db to create the obj.
1. query db to get anime with titles, openings, and endings

'''

def create_game_room() -> GameRoom:
    ...


def fetch_animes():
    with next(get_db()) as db:
        animes = (
            db.query(Anime)
            .options(
                joinedload(Anime.openings),
                joinedload(Anime.endings),
                joinedload(Anime.titles),
            )
            .limit(10)
            .all()
        )
        clean = []
        for anime in animes:
            clean.append(CleanList.model_validate(anime))

        return [c.model_dump() for c in clean]


        # r = get_client()
        # for anime in data:´
        #     redis_mapping = {
        #         "anime": json.dumps(anime["anime"]),
        #         "openings": json.dumps(anime["openings"]),
        #         "endings": json.dumps(anime["endings"]),
        #         "titles": json.dumps(anime["titles"]),
        #     }
        #     r.hset("test", mapping=redis_mapping)
        # return animes