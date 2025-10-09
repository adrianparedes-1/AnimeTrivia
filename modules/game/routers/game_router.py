from fastapi import APIRouter, Request, HTTPException, Response, status
from modules.game.dtos.game_room_dto import Guess
from modules.game.services.game_room_service import create_game_room
from modules.game.services.game_logic_service import selection, guessing
import logging

logger = logging.getLogger(__name__)



router = APIRouter(
    prefix="/game", 
    tags=["Game"]
)


@router.post("")
def start_game(request: Request):
    necessary_player_info = {
        "id": request.state.user["id"],
        "username": request.state.user["username"],
        "display_name": request.state.user["display_name"]
    }
    try:
        create_game_room([necessary_player_info])
    except Exception as e:
        logger.exception("starting game room failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"starting game room failed: {e}"
        )
    return Response(
        status_code=status.HTTP_200_OK
    )


@router.post("/guess")
# def logic(name: Guess):
#     if name:
#         try:
#             result = guessing(name)
#         except Exception as e:
#             logger.exception("guessing logic failed")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"guessing logic failed: {e}"
#             )
#         return Response(
#             status_code=status.HTTP_200_OK,
#             content=result
#         )
#     else:
#         return Response(
#                 status_code=status.HTTP_200_OK,
#                 content="Player did not submit a guess"
#             )
def logic():
    selection()