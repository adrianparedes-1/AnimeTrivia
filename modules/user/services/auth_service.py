from dependencies.redis_client import delete_keys_containing, get_client
import os, httpx
from dotenv import load_dotenv
from utils.state_generator import create_state
from contextlib import asynccontextmanager
from utils.pkce_code_utils import *
from modules.user.dtos.auth_response_dto import SpotifyLoginResponse

load_dotenv()

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SERVICE")
redirect_uri = os.getenv("CALLBACK_URL")
spotify_auth_url = "https://accounts.spotify.com/authorize"
scope="user-read-email user-read-private"

@asynccontextmanager
async def process_login():
    async with httpx.AsyncClient() as client:
        code = code_verifier()
        code_challenge = code_hashing(code)
        state = create_state()
        response: SpotifyLoginResponse = await client.get(
            url=spotify_auth_url,
            params={
                "client_id": client_id,
                "response_type": code,
                "redirect_uri": redirect_uri,
                "state": state,
                "scope": scope,
                "code_challenge_method": "S256",
                "code_challenge": code_challenge
            })
        
        yield response



async def exchange_code_token(code: str):
    async with httpx.AsyncClient() as client:
        r = await client.post("https://accounts.spotify.com/api/token",
                          headers={
                              "Authorization" : f"Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}",
                              "Content-Type" : "application/x-www-form-urlencoded"
                              },
                          data={
                              "grant_type": "authorization_code",
                              "code" : f"{code}",
                              "redirect_uri" : f"{redirect_uri}"
                          })
    
    return r


# @asynccontextmanager
# async def get_sso():
#     async with CustomSpotifySSO(
#         client_id=client_id,
#         client_secret=client_secret,
#         redirect_uri=redirect_uri,
#         scope="user-read-email user-read-private"
#     ) as sso:
#         yield sso






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