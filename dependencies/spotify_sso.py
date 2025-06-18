from fastapi_sso.sso.spotify import SpotifySSO
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SERVICE")
redirect_uri = "http://127.0.0.1:8000/auth/callback"

def sso_dependency():
    return SpotifySSO (
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-email user-read-private"
    )
