import httpx, asyncio
from modules.anime.models.anime_orm_model import Anime
from modules.anime.models.openings_orm_model import Openings
from modules.anime.models.endings_orm_model import Endings
from modules.anime.dtos.themes_dto import Data
from db.session_manager import get_db

async def themes_service():
    async with httpx.AsyncClient() as async_client:
        with next(get_db()) as db:
            existing_animes = {n for n, in
                db.query(Anime.mal_id).all()
            }
            # print(type(existing_animes))
            # print(len(existing_animes))

            anime_dict = {}
            for anime in existing_animes:
                response = await async_client.get(f"https://api.jikan.moe/v4/anime/{anime}/themes")
                validated_themes_obj = Data.model_validate(response.json())
                if validated_themes_obj and validated_themes_obj.data:
                    anime_dict[f"{anime}:openings"] = validated_themes_obj.data.openings
                    anime_dict[f"{anime}:endings"] = validated_themes_obj.data.endings
                await asyncio.sleep(0.2)
            '''
            for every anime, i want to create an instance with the key being the anime and values being the openings and endings
            '''
            anime_objs = db.query(Anime).filter(Anime.mal_id.in_(existing_animes)).all()
            anime_map = {anime.mal_id: anime for anime in anime_objs}

            bulk_openings = []
            bulk_endings = []

            existing_openings = {o.title for o in db.query(Openings).all()}
            existing_endings = {e.title for e in db.query(Endings).all()}

            batch_openings = set()
            batch_endings = set()

            for anime_key, songs in anime_dict.items():
                anime_id = int(anime_key.split(':')[0])
                anime_obj = anime_map.get(anime_id)
                if not anime_obj:
                    continue
                if 'openings' in anime_key:
                    existing_titles = {o.title.strip().lower() for o in anime_obj.openings}
                    for song in songs:
                        normalized_song = song.strip().lower() if song else None
                        if (
                            song
                            and normalized_song not in {t.strip().lower() for t in existing_openings}
                            and normalized_song not in existing_titles
                            and normalized_song not in batch_openings
                        ):
                            opening = Openings(title=song)
                            anime_obj.openings.append(opening)
                            bulk_openings.append(opening)
                            batch_openings.add(normalized_song)
                if 'endings' in anime_key:
                    existing_titles = {e.title.strip().lower() for e in anime_obj.endings}
                    for song in songs:
                        normalized_song = song.strip().lower() if song else None
                        if (
                            song
                            and normalized_song not in {t.strip().lower() for t in existing_endings}
                            and normalized_song not in existing_titles
                            and normalized_song not in batch_endings
                        ):
                            ending = Endings(title=song)
                            anime_obj.endings.append(ending)
                            bulk_endings.append(ending)
                            batch_endings.add(normalized_song)

            if bulk_openings or bulk_endings:
                db.add_all(bulk_openings + bulk_endings)
                db.commit()
