from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from dependencies.token_service import create_tokens
from ..services.auth_service import get_sso, logout_service
import logging

from modules.user.services.user_service import (
    create,
    save_in_redis
)

logger = logging.getLogger()

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)


@router.get("")
async def login():
    sso = await get_sso()
    return await sso.get_login_redirect()
        

@router.get("/callback")
async def callback(request: Request):
    sso = await get_sso()
        # try: #catch any failure with the oauth flow
        #     user = await sso.verify_and_process(request)
        # except Exception as e:
        #     logger.exception(e)
    # save user in db
    user = await sso.verify_and_process(request)
    user_db = create(user)
    # initialize local variables to save spotify tokens
    spotify_access_token = sso._custom_access_token
    spotify_refresh_token = sso._custom_refresh_token
    # create backend tokens
    app_access_token, app_refresh_token = create_tokens(user_db.model_dump())
    # print(f"Test ------------- {app_access_token}")
    # print(f"Test ------------- {app_refresh_token}")
    # save all tokens in redis
    if app_access_token and app_refresh_token:
        save_in_redis(
            user_db.id,
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
    print(user_id)
    logout_service(user_id)
    return Response (status_code=204)