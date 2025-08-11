from fastapi import APIRouter
from modules.game.dtos.game_room_dto import GameRoom
from modules.game.services.game_room_service import create_game_room, fetch_animes


router = APIRouter(
    prefix="/game", 
    tags=["Game"]
)


@router.get("")
def start_game():
    # game_room_instance = GameRoom()
    # return game_room_instance
    return fetch_animes()