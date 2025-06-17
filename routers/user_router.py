from fastapi import APIRouter, Request
from fastapi_sso.sso.spotify import SpotifySSO
from dtos.user_long_dto import UserLogin
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SERVICE")
redirect_uri = "http://127.0.0.1:8000/auth/complete/spotify"


router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)


spotify_sso = SpotifySSO(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-email user-read-private"
)


@router.get("")
async def login():
    return await spotify_sso.get_login_redirect()


@router.get("/complete/spotify")
async def callback(request: Request):
    async with spotify_sso:
        user = await spotify_sso.verify_and_process(request)
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "picture": user.picture,
    }
