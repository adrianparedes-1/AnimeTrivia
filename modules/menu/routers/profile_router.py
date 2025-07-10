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
async def profile(request: Request):
    async with show_profile(request.state.user) as profile:
        '''
        service should get the user id that matches the one in db and search for it. once found, set a return dto to response
        we are doing async because we need to wait for the fetch operation to complete before we return anything
        '''
        await ...


@router.post("")
def log_out(request: Request):
    ...
    '''
    delete tokens from redis
    log activity
    redirect to login url
    '''