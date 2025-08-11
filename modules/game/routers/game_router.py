from fastapi import APIRouter
from modules.game.dtos.game_room_dto import GameRoom


router = APIRouter(
    prefix="/game", 
    tags=["Game"]
)


@router.get("")
def start_game():
    game_room_instance = GameRoom()
    return game_room_instance
    