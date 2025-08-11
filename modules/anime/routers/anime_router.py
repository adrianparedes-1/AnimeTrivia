from fastapi import APIRouter, Response, status, HTTPException
from modules.anime.services.anime_service import populate_anime_table
from modules.anime.services.themes_service import themes_service
import logging
'''
call a service that gets the info from MAL api and writes it to db
'''
router = APIRouter(
    prefix="/anime", 
    tags=["Anime"]
)
logger = logging.getLogger(__name__)

@router.post("")
async def add_animes():
    try:
        await populate_anime_table()
    except Exception as exc:
        logger.exception("populate_anime_table failed")
        raise HTTPException(
            status_code=500,
            detail=f"Populating anime table failed: {exc}"
        )
    return Response(
        status_code=status.HTTP_200_OK,
        content="Animes added to DB successfully.",
        media_type="text/plain",
    )


@router.post("/themes")
async def add_themes():
    try:
        await themes_service()
    except Exception as exc:
        logger.exception("themes_service failed")
        raise HTTPException(
            status_code=500,
            detail=f"Populating openings/endings tables failed: {exc}"
        )
    return Response(
        status_code=status.HTTP_200_OK,
        content="Openings and Endings added to DB successfully.",
        media_type="text/plain",
    )