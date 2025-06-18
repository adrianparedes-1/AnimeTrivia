from fastapi import APIRouter, Request, Depends
from fastapi_sso.sso.spotify import SpotifySSO
from modules.user.dtos.user_response_dto import UserResponseDTO
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
            response_model=UserResponseDTO
            )
async def callback(
    request: Request, 
    sso: SpotifySSO = Depends(sso_dependency)
    ):
    async with sso:
        user = await sso.verify_and_process(request)
    return UserResponseDTO(
        **user.model_dump()
    )