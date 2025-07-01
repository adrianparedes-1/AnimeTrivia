from fastapi import APIRouter, Depends, Request
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

@router.get("")
def test():
    return "placeholder for frontend endpoint"


'''
in the profile endpoint, i'm assuming the middleware has already been set and the token is being sent properly from the frontend.
    This is the middleware logic that extracts the token and checks it: 
    token = request.headers.get("authorization")
    response = oauth2.check_token(token)

check_token returns a decoded token which i need to get the username from the payload


'''

@router.get("/profile")
async def profile(request: Request):
    async with show_profile(request.body("username")) as profile: # this is just to wait for the username to be extracted from the jwt
        ...