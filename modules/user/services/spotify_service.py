from dependencies.redis_client import get_client
from fastapi import status

def fetch_spotify_token(sid: str):
    if not sid:
        return (
            "Cookie was not received",
            status.HTTP_400_BAD_REQUEST
        )
    r = get_client()
    token = r.hget(f"session:{sid[4:]}", "spotify_access_token")
    return token