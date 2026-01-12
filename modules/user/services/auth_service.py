from dependencies.redis_client import delete_keys_containing
from dependencies.spotify_sso import (
    client_id,
    client_secret,
    redirect_uri,
    CustomSpotifySSO
)
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_sso():
    async with CustomSpotifySSO(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-email user-read-private"
    ) as sso:
        yield sso

def logout_service(user_id: int):
    '''
    Docstring for logout_service:
    '''
    delete_keys_containing(user_id)