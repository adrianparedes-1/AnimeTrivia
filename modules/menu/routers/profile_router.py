from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from modules.menu.dtos import player_profile_dto
from modules.menu.services.profile_service import show_profile


router = APIRouter(
    prefix="/profile", 
    tags=["Player Profile"]
)

@router.get("")
def profile(request: Request):
    # print(request.state.user)
    profile = show_profile(request.state.user)
    return profile


# @router.post("")
# def log_out(request: Request):
#     ...
#     '''
#     delete tokens from redis
#     log activity
#     redirect to login url
#     '''