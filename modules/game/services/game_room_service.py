from db.session_manager import get_db
from sqlalchemy.orm import joinedload
from modules.game.dtos.game_room_dto import GameRoom
from modules.anime.models.anime_orm_model import Anime

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
        # convert to dicts for testing
        data = []
        for anime in animes:
            data.append({
                "anime": {
                    c.name: getattr(anime, c.name)
                    for c in anime.__table__.columns
                },
                "openings": [
                    {c.name: getattr(op, c.name) for c in op.__table__.columns}
                    for op in anime.openings
                ],
                "endings": [
                    {c.name: getattr(ed, c.name) for c in ed.__table__.columns}
                    for ed in anime.endings
                ],
                "titles": [
                    {c.name: getattr(title, c.name) for c in title.__table__.columns}
                    for title in anime.titles
                ]
            })

        return data