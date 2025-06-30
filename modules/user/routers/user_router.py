from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from dependencies.spotify_sso import (
    client_id,
    client_secret,
    redirect_uri,
    CustomSpotifySSO
)
from dependencies.token_service import create_tokens
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
    spotify_access_token = sso._custom_access_token
    spotify_refresh_token = sso._custom_refresh_token
    app_access_token, app_refresh_token = create_tokens(user.model_dump())
    
    if user and app_access_token:
        # add logic for creating access and refresh tokens for this backend service so I can save them in same hashmap as the spotify tokens in redis
        save_in_redis(
            user.id,
            app_access_token,
            app_refresh_token,
            spotify_access_token,
            spotify_refresh_token
            )

    return RedirectResponse(
        url=URL("/auth/token")
    )

@router.get("/token")
async def get_token(request: Request):
    print("hello world")
    
    # https://api.spotify.com/api/token