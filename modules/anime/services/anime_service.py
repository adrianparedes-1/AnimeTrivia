import httpx, asyncio
from db.session_manager import get_db
from db.db_helpers import construct_orm_model_from_list, construct_parent_with_children
from modules.anime.models import (
    anime_orm_model,
    genres_orm_model,
    image_orm_model,
    studios_orm_model,
    titles_orm_model,
    topical_themes_orm_model,
    trailer_orm_model
)

from modules.anime.dtos.anime_dto import Data
MAL_URL = "https://api.jikan.moe/v4/top/anime"
PAGES = 22 
sleep_timer = 2


'''
i want to  send a get request to the mal api and get a json
since the json is paginated, i want to continue to send requests until page 21
so that i can have 500~ animes. I want to make the request process async
bc i want to wait until the info is retrieved and ready for me to write to db.
So i can use httpx with an async context manager inside of a for loop with
the page as the counter. Once it reaches 21, then exit.

'''

async def populate_anime_table():
    async with httpx.AsyncClient() as async_client:
        for page in range(1,PAGES):
            try:
                response = await async_client.get(f"{MAL_URL}", params={"page": page})
                validated_animes_obj = Data.model_validate(response.json())
                for anime in validated_animes_obj.animes:
                    with next(get_db()) as db:
                        existing = db.query(anime_orm_model.Anime).filter(
                            anime.mal_id == anime_orm_model.Anime.mal_id
                        ).first()
                        if not existing:
                            key_map = {
                                "topical_themes": construct_orm_model_from_list(
                                    anime.topical_themes,
                                    topical_themes_orm_model.TopicalThemes,
                                    topical_themes_orm_model.TopicalThemes.name,
                                    lambda tt: tt.name
                                ),
                                "titles": construct_orm_model_from_list(
                                    anime.titles,
                                    titles_orm_model.Titles,
                                    titles_orm_model.Titles.name,
                                    lambda t: t.name
                                ),
                                "studios": construct_orm_model_from_list(
                                    anime.studios,
                                    studios_orm_model.Studios,
                                    studios_orm_model.Studios.name,
                                    lambda s: s.name    
                                ),
                                "genres": construct_orm_model_from_list(
                                    anime.genres,
                                    genres_orm_model.Genres,
                                    genres_orm_model.Genres.genre,
                                    lambda g: g.genre
                                )
                            }
                            # scalar_fields = anime.model_dump(
                            #     exclude=set(key_map.keys()) | {"trailer", "image"}
                            # )
                            # scalar_fields["trailer"] = trailer_orm_model.Trailer(**anime.trailer.model_dump()) if anime.trailer else None
                            # scalar_fields["image"] = image_orm_model.Image(**anime.image.jpg.model_dump()) if anime.image.jpg else None
                            scalar_fields = {
                                "mal_id":        anime.mal_id,
                                "name":          anime.name,
                                "rank":          anime.rank,
                                "score":         anime.score,
                                "scored_by":     anime.scored_by,
                                "popularity":    anime.popularity,
                                "times_favorited": anime.times_favorited,
                                "members_MAL":   anime.members_MAL,
                                "synopsis":      anime.synopsis,
                                "release_year":  anime.release_year,
                                "release_season":anime.release_season,
                                "trailer":      trailer_orm_model.Trailer(**anime.trailer.model_dump()) if anime.trailer else None,
                                "image":        image_orm_model.Image(**anime.image.jpg.model_dump()) if anime.image and anime.image.jpg else None,
                            }

                            construct_parent_with_children(
                                anime_orm_model.Anime,
                                scalar_fields,
                                key_map
                            )
                        else:
                            continue
            except Exception:
                raise
            await asyncio.sleep(sleep_timer)