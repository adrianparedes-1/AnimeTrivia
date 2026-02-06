from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from ..services.auth_service import logout_service, process_login, exchange_code_token, delete_session
from ..services.spotify_service import fetch_spotify_token
import logging, httpx

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
    
    if not code:
        error = request.query_params.get("error")
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error
        )
    
    sid = await exchange_code_token(code, state)
    delete_session()
    
    response = RedirectResponse(
        url="http://127.0.0.1:5173/home",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(
        key="sid",
        value=sid,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    return response

@router.get("/spotify/token")
def get_spotify_token(request: Request):
    sid = request.headers.get("Cookie")
    token = fetch_spotify_token(sid)
    return token


@router.delete("/logout")
async def logout(request: Request):
    user_id = request.state.user["id"]
    logout_service(user_id) #add try/catch
    return Response (
        status_code=status.HTTP_204_NO_CONTENT
    )