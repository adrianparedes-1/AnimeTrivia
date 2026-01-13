from dependencies.redis_client import delete_keys_containing, get_client
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


def set_code(code: str):
    r = get_client()
    r.setex(
        name=f"code: {code}",
        time=300,
        value=1
    )

def check_code(code: str):
    r = get_client()
    if r.exists(f"code: {code}"):
        return 204

def delete_state():
    r = get_client()
    r.delete("state")

def logout_service(user_id: int):
    delete_keys_containing(user_id)