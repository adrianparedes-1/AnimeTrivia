from db.session_manager import get_db
from sqlalchemy.orm import joinedload
from sqlalchemy import func, exists
from modules.game.dtos.clean_retrieval import AnimeRedis
from modules.anime.models.anime_orm_model import Anime
from modules.anime.models.openings_orm_model import Openings
from modules.anime.models.endings_orm_model import Endings
from modules.game.dtos.game_room_dto import GameRoom
from dependencies.redis_client import get_client
from typing import List
import uuid, random
'''
create a game room obj using the Game Room DTO.
We will query db to create the obj.
1. query db to get anime with titles, openings, and Endingss
2. create hash in redis with game room info (game room session)
'''
r = get_client()

def get_recent_animes(player_id: int):
    '''
    Fetch the recent animes in cache to avoid selecting the same songs.
    '''
    try:
        return r.json().get(f"recent_animes: {player_id}")
    except:
        return []

def add_to_recent_animes(animes, players: List[dict]):
    '''
    Add animes to recent animes list in cache.
    '''
    for player in players:
        cached_animes = get_recent_animes(player["id"])
        if not cached_animes:
            r.json().set(f"{player["id"]}: recent_animes", "$", cached_animes)
            r.expire(f"{player["id"]}: recent_animes", 86400)
        else:
            cached_animes.extend(anime for anime in animes)
            r.json().set(f"{player["id"]}: recent_animes", "$", cached_animes)
            r.expire(f"{player["id"]}: recent_animes", 86400)

def create_game_room(players: List[dict]):
    '''
    Creates game room in redis
    ''' 
    animes = fetch_animes(players)
    room_id = uuid.uuid4()
    game_room = {
        "players": players,
        "anime_list": animes
    }
    r.json().set(f"game_room:{room_id}", "$", game_room)
    r.expire(f"game_room:{room_id}", 3600)
    add_to_recent_animes(animes, players)
    return room_id

def fetch_animes(players: List[dict]) -> List[dict]:
    count: int = 10
    for player in players:
        cached_animes = get_recent_animes(player["id"])
        with next(get_db()) as db:
            if cached_animes:
                animes_list = (anime.get("anime") for anime in cached_animes)
                animes = (
                    db.query(Anime)
                    .filter(Anime.name.not_in(animes_list))
                    .filter(
                        (Anime.openings.any()) | 
                        (Anime.endings.any())
                    )
                    .order_by(func.random())
                    .options(
                        joinedload(Anime.openings),
                        joinedload(Anime.endings),  
                        joinedload(Anime.titles),
                    )
                    .limit(count)
                    .all()
                )
            else:
                animes = (
                    db.query(Anime)
                    .filter(
                        (Anime.openings.any()) | 
                        (Anime.endings.any())
                    )
                    .order_by(func.random())
                    .options(
                        joinedload(Anime.openings),
                        joinedload(Anime.endings),
                        joinedload(Anime.titles),
                    )
                    .limit(count)
                    .all()
                )
            
            clean = [AnimeRedis.model_validate(anime) for anime in animes]
            final_obj = [c.model_dump() for c in clean]
            return final_obj
