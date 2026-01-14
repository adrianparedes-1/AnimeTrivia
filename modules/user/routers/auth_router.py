from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from dependencies.token_service import create_tokens
from ..services.auth_service import logout_service, set_code, check_code, process_login
import logging
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

logger = logging.getLogger()
spotify_auth_url = "https://accounts.spotify.com/authorize"
router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)


@router.get("")
async def login():
    async with process_login():
        return RedirectResponse(
            spotify_auth_url,
            303
            )
    # test_state()
    # async with CustomSpotifySSO(
    #     client_id=client_id,
    #     client_secret=client_secret,
    #     redirect_uri=redirect_uri,
    #     scope="user-read-email user-read-private"
    # ) as sso:
    #     print(f"Test: {sso._generated_state}")
        # return await sso.get_login_redirect()
        

@router.get("/callback")
async def callback(request: Request):

    #stop duplicate call to verify_and_process
    code = request.query_params.get("code")
    response = check_code(code)
    if response == 204:
        return Response(status_code=200)
    set_code(code)

    async with CustomSpotifySSO(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-email user-read-private",
    ) as sso:
        user = await sso.verify_and_process(request)
    # save user in db
    user_db = create(user)
    # initialize local variables to save spotify tokens
    spotify_access_token = sso._custom_access_token
    spotify_refresh_token = sso._custom_refresh_token
    # create backend tokens
    app_access_token, app_refresh_token = create_tokens(user_db.model_dump())
    # print(f"Test ------------- {app_access_token}")
    # print(f"Test ------------- {app_refresh_token}")
    # save all tokens in redis
    if app_access_token and app_refresh_token:\
        save_in_redis(
            user_db.id,
            app_access_token,
            app_refresh_token,
            spotify_access_token,
            spotify_refresh_token
            )
    # redirect to complete endpoint
    return RedirectResponse(
        url=URL(
            "/complete"
        ),
        status_code=status.HTTP_204_NO_CONTENT
    )

# redirect to menu router
@router.get("/complete")
def get_token():
    return RedirectResponse(
        url=URL("/home")
    )

@router.get("/user")
def get_user(request: Request):
    return request.state.user


@router.delete("/logout")
async def logout(request: Request):
    user_id = request.state.user["id"]
    logout_service(user_id) #add try/catch
    return Response (
        status_code=status.HTTP_204_NO_CONTENT
    )