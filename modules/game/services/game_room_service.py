from db.session_manager import get_db
from sqlalchemy.orm import joinedload, load_only
from modules.game.dtos.game_room_dto import GameRoom
from modules.game.dtos.clean_retrieval import CleanList
from modules.anime.models.anime_orm_model import Anime
from dependencies.redis_client import get_client
from typing import Mapping, List
import json, uuid
'''
create a game room obj using the Game Room DTO.
We will query db to create the obj.
1. query db to get anime with titles, openings, and endings
2. create hash in redis with game room info (game room session)
'''

def create_game_room(players: List):
    '''
    Creates game room in redis
    '''
    animes = fetch_animes()
    room_id = uuid.uuid4()
    game_room = {
        "players": players,
        "anime_list": animes
    }
    r = get_client()
    r.json().set(f"game_room:{room_id}", "$", game_room)
    r.expire(f"game_room:{room_id}", 15)


def fetch_animes() -> Mapping:
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

        final_obj = [c.model_dump() for c in clean]

        return final_obj


def redis_test(animes: Mapping):
    r = get_client()
    r.json().set("current_list", "$", animes)
