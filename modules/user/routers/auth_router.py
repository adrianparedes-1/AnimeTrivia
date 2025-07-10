from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from dependencies.token_service import create_tokens
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
        scope="user-read-email user-read-private offline-access"
    ) as sso:
        user = await sso.verify_and_process(request)

    # save user in db
    create(user)
    # initialize local variables to save spotify tokens
    spotify_access_token = sso._custom_access_token
    spotify_refresh_token = sso._custom_refresh_token
    
    # create backend tokens
    app_access_token, app_refresh_token = create_tokens(user.model_dump())
    # print(f"Test ------------- {app_access_token}")
    # print(f"Test ------------- {app_refresh_token}")
    # save all tokens in redis
    if app_access_token and app_refresh_token:
        save_in_redis(
            user.id,
            app_access_token,
            app_refresh_token,
            spotify_access_token,
            spotify_refresh_token
            )

    # redirect to complete endpoint
    return RedirectResponse(
        url=URL("/auth/complete")
    )

# redirect to menu router
@router.get("/complete")
async def get_token():
    return RedirectResponse(
        url=URL("/home")
    )