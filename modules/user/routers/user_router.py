from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from dependencies.spotify_sso import (
    client_id,
    client_secret,
    redirect_uri,
    CustomSpotifySSO
)
from modules.user.services.user_service import (
    create,
    save_in_redis
)

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)

@router.get("")
async def login():
    async with CustomSpotifySSO(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-email user-read-private"
    ) as sso:
        return await sso.get_login_redirect()


@router.get("/callback")
async def callback(request: Request):
    async with CustomSpotifySSO(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-email user-read-private"
    ) as sso:
        user = await sso.verify_and_process(request)
    create(user)
    save_in_redis(
        user.id,
        sso._custom_access_token,
        sso._custom_refresh_token
        )

    return RedirectResponse(
        url=URL("/auth/token")
    )

@router.get("/token")
async def get_token(request: Request):
    print("hello world")
    
    # https://api.spotify.com/api/token