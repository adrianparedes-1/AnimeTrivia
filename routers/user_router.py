from fastapi import APIRouter, Request, Depends
from fastapi_sso.sso.spotify import SpotifySSO
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

@router.get("/callback")
async def callback(
    request: Request, 
    sso: SpotifySSO = Depends(sso_dependency)
    ):
    async with sso:
        user = await sso.verify_and_process(request)
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "display_name": user.display_name,
        "provider": user.provider
    }