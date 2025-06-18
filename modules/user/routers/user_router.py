from fastapi import APIRouter, Depends, Request
from fastapi_sso.sso.spotify import SpotifySSO
from modules.user.dtos import (
    user_response_dto
)
from dependencies.spotify_sso import sso_dependency


router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)

@router.get("")
async def login(
    sso: SpotifySSO = Depends(sso_dependency)
    ):
    async with sso:
        return await sso.get_login_redirect()
    

@router.get("/callback",
            response_model=user_response_dto.UserResponseDTO
            )
async def callback(
    request: Request, # verify_and_process() method expects a fastapi Request object so this is the easiest method rather than defining a pydantic dto
    sso: SpotifySSO = Depends(sso_dependency)
    ):
    async with sso:
        user = await sso.verify_and_process(request)
    return user_response_dto.UserResponseDTO(
        **user.model_dump()
    )