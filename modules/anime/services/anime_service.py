import httpx, asyncio
from db.session_manager import get_db
from modules.anime.models.anime_orm_model import Anime
from modules.anime.dtos.anime_dto import AnimeDto, Data

MAL_URL = "https://api.jikan.moe/v4/top/anime"
PAGES = 22 


'''
i want to  send a get request to the mal api and get a json
since the json is paginated, i want to continue to send requests until page 21
so that i can have 500~ animes. I want to make the request process async
bc i want to wait until the info is retrieved and ready for me to write to db.
So i can use httpx with an async context manager inside of a for loop with
the page as the counter. Once it reaches 21, then exist.

'''

async def populate_db():
    response = await httpx.AsyncClient().get(f"{MAL_URL}", params={"page": 1})
    validated_animes_obj = Data.model_validate(response.json())
    return validated_animes_obj.animes
    # async with httpx.AsyncClient() as async_client:
    #     for page in range(1,PAGES):
    #         try:
    #             response = await async_client.get(f"{MAL_URL}", params={"page": page})
    #             animes: AnimeDto = response.content
    #             print(animes.mal_id)
    #             # with next(get_db()) as db:
    #             #     existing = db.query(Anime).filter(
    #             #         animes.mal_id == Anime.mal_id
    #             #     ).first()
    #             #     if not existing:
    #             #         new_anime = Anime(
    #             #             **animes.model_dump()
    #             #         )
    #             #         db.add(new_anime)
    #             #         db.commit()
    #         except Exception:
    #             # retry 3 times then give up
    #             raise
    #         await asyncio.sleep(2)
    