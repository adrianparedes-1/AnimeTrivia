from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL

from ..services.auth_service import logout_service, check_session, process_login, exchange_code_token, fetch_user_info
import logging, httpx
import fastapi_sso
from dependencies.spotify_sso import (
    client_id,
    client_secret,
    redirect_uri,
    CustomSpotifySSO
)


logger = logging.getLogger()

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)

@router.get("")
async def login():
    spotify_auth_url, params = process_login()
    return RedirectResponse(
        url=httpx.URL(
            spotify_auth_url,
            params=params
        ),
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    #this happens on any error so i can do a try catch
    if not code:
        error = request.query_params.get("error")
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error
        )
    # r = check_session()
    # if r == 204:
    #     return RedirectResponse(
    #         url=URL(
    #             "/home"
    #         ),
    #         status_code=status.HTTP_303_SEE_OTHER
    #     )
    
    await exchange_code_token(code, state)
    # # print(response["access_token"])
    # await fetch_user_info(response["access_token"])

    
    # return response

    # async with CustomSpotifySSO(
    #     client_id=client_id,
    #     client_secret=client_secret,
    #     redirect_uri=redirect_uri,
    #     scope="user-read-email user-read-private",
    # ) as sso:
    #     user = await sso.verify_and_process(request)

    # redirect to complete endpoint
    return RedirectResponse(
        url=httpx.URL(
            "/home",
        ),
        status_code=status.HTTP_303_SEE_OTHER
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