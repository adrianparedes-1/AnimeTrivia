from fastapi import APIRouter, Depends
from modules.menu.dtos import player_profile_dto

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



@router.get("/profile")
def profile():
    show_profile()