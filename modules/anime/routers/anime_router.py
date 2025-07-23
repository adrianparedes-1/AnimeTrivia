from fastapi import APIRouter, Request, Response
from modules.anime.services.anime_service import populate_db
'''
call a service that gets the info from MAL api and writes it to db

'''
router = APIRouter(
    prefix="/anime", 
    tags=["Anime"]
)

@router.post("/add")
async def add():
    return await populate_db()