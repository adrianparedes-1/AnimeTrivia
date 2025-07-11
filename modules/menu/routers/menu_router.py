from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from modules.menu.dtos import player_profile_dto
from modules.menu.services.profile_service import show_profile

'''
main menu: 
play
profile
logout

'''
router = APIRouter(
    prefix="/home", 
    tags=["Menu"]
)

'''
in the profile endpoint, i'm assuming the middleware has already been set and the token is being sent properly from the frontend.
    This is the middleware logic that extracts the token and checks it: 
    token = request.headers.get("authorization")
    response = oauth2.check_token(token)

check_token returns a decoded token which i need to get the username from the payload

'''

# @router.get("/")
# def read_profile(request: Request):
#     return {"user": request.state.user}


@router.get("")
async def profile(request: Request):
    return RedirectResponse(
            url=URL("/profile")
        )

@router.get("/play")
def read_profile(request: Request):
    return {"user": request.state.user}