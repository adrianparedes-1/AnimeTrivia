import httpx, asyncio
from db.session_manager import get_db
from modules.anime.models import (
    anime_orm_model,
    ending_orm_model,
    genre_orm_model,
    image_orm_model,
    opening_orm_model,
    studio_orm_model,
    theme_orm_model,
    title_orm_model,
    topical_theme_orm_model,
    trailer_orm_model
)
from modules.anime.dtos.anime_dto import Data, AnimeDto
MAL_URL = "https://api.jikan.moe/v4/top/anime"
PAGES = 22 
sleep_timer = 2


'''
i want to  send a get request to the mal api and get a json
since the json is paginated, i want to continue to send requests until page 21
so that i can have 500~ animes. I want to make the request process async
bc i want to wait until the info is retrieved and ready for me to write to db.
So i can use httpx with an async context manager inside of a for loop with
the page as the counter. Once it reaches 21, then exist.

'''
# def construct_orm_model(anime_dto: AnimeDto) -> anime_orm_model.Anime:
#     return anime_orm_model.Anime (
#         **anime_dto.model_dump(
#             exclude=["topical_themes",
#                     "trailer",
#                     "titles",
#                     "genres",
#                     "studios",
#                     "images",
#                     ]),
#         # rank=anime_dto.rank if anime_dto.rank is not
#         # topical_themes=[topical_theme_orm_model.TopicalTheme(**t.model_dump()) for t in anime_dto.topical_themes] if anime_dto.topical_themes else [],
#         # trailer=trailer_orm_model.Trailer(**anime_dto.trailer.model_dump()) if anime_dto.trailer else None,
#         # titles=[title_orm_model.Title(**t.model_dump()) for t in anime_dto.titles] if anime_dto.titles else [],
#         # genres=[genre_orm_model.Genre(**g.model_dump()) for g in anime_dto.genres] if anime_dto.genres else [],
#         # studios=[studio_orm_model.Studio(**s.model_dump()) for s in anime_dto.studios] if anime_dto.studios else [],
#         # images=image_orm_model.Image(**anime_dto.images.jpg.model_dump()) if anime_dto.images.jpg else None
#     )


def construct_orm_model(dto, orm_model, exclude = list[str]):
    return orm_model (
        **dto.model_dump(exclude=exclude))

async def populate_anime_table():
    async with httpx.AsyncClient() as async_client:
        for page in range(1, PAGES):
            try:
                response = await async_client.get(f"{MAL_URL}", params={"page": page})
                validated_animes_obj = Data.model_validate(response.json())
                for anime in validated_animes_obj.animes:
                    with next(get_db()) as db:
                        existing = db.query(anime_orm_model.Anime).filter(
                            anime.mal_id == anime_orm_model.Anime.mal_id
                        ).first()
                        if not existing:
                            new_anime = construct_orm_model(
                            dto=AnimeDto, 
                            orm_model=anime_orm_model.Anime,
                            exclude=["topical_themes",
                                            "trailer",
                                            "titles",
                                            "genres",
                                            "studios",
                                            "images",
                                            ])
                            db.add(new_anime)
                            db.commit()
                        else:
                            continue
            except Exception:
                raise
            await asyncio.sleep(sleep_timer)


async def populate_table(pages: int, sleep_timer: int, dto, url: str):
    async with httpx.AsyncClient() as async_client:
        for page in range(1,pages):
            try:
                response = await async_client.get(f"{url}", params={"page": page})
                validated_obj = dto.model_validate(response.json())
                for anime in validated_obj.animes:
                    with next(get_db()) as db:
                        existing = db.query(anime_orm_model.Anime).filter(
                            anime.mal_id == anime_orm_model.Anime.mal_id
                        ).first()
                        if not existing:
                            new_anime = construct_orm_model(
                                dto=AnimeDto, 
                                orm_model=anime_orm_model.Anime,
                                exclude=["topical_themes",
                                                "trailer",
                                                "titles",
                                                "genres",
                                                "studios",
                                                "images",
                                                ])
                            db.add(new_anime)
                            db.commit()
                        else:
                            continue
            except Exception:
                raise
            await asyncio.sleep(sleep_timer)