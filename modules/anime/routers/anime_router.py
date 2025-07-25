from fastapi import APIRouter, Response, status
from modules.anime.services.anime_service import populate_anime_table
'''
call a service that gets the info from MAL api and writes it to db

'''
router = APIRouter(
    prefix="/anime", 
    tags=["Anime"]
)

@router.post("")
async def add_animes():
    try:
        await populate_anime_table()
    except Exception:
        return Exception
    return Response(
        status_code=status.HTTP_200_OK, 
        content="Animes added to DB sucessfully."
        )



@router.post("/themes")
async def add_themes():
    ...