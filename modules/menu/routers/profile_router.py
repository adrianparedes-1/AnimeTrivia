from fastapi import APIRouter, Request, status
from modules.menu.services.profile_service import show_profile
from dependencies.redis_client import delete_keys_containing


router = APIRouter(
    prefix="/profile", 
    tags=["Profile"]
)

@router.get("")
def profile(request: Request):
    # print(request.state.user)
    profile = show_profile(request.state.user)
    return profile


@router.get("/logout")
def log_out(request: Request):
    delete_keys_containing(request.state.user["id"])
    return status.HTTP_200_OK

# TODO: add activity logs