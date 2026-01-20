from dependencies.redis_client import delete_keys_containing, get_client
import os, httpx
from dotenv import load_dotenv
from utils.state_generator import create_state
from utils.pkce_code_utils import code_verifier, code_challenge

load_dotenv()

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SERVICE")
redirect_uri = os.getenv("CALLBACK_URL")
spotify_auth_url = "https://accounts.spotify.com/authorize"
spotify_exchange_url = "https://accounts.spotify.com/api/token"
scope="user-read-email user-read-private"

def process_login():
    verifier = code_verifier()
    print("code saved in redis:", verifier)
    state = create_state()
    create_session(verifier, state)
    code_chall = code_challenge(verifier)
    params={
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": scope,
            "code_challenge_method": "S256",
            "code_challenge": code_chall
        }
    
    return (
        spotify_auth_url,
        params
    )

async def exchange_code_token(code: str, state: str):
    verifier = get_code(state)
    async with httpx.AsyncClient() as client:
        r = await client.post(
            url=spotify_exchange_url,
            headers={
            "Content-Type" : "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "code_verifier": verifier
            }
        )
    print("Response:", r.json())
    return r.json()

def create_session(code_verifier: str, state: str):
    r = get_client()
    r.setex(
        name=f"code:{state}",
        time=300,
        value=code_verifier
    )

def get_code(state: str) -> str:
    r = get_client()
    code = r.get(f"code:{state}")
    print("Getting code from redis:", code)
    return code

def check_session():
    r = get_client()
    if r.exists(f"code:*"):
        return 204

def delete_session():
    r = get_client()
    r.delete("")

def logout_service(user_id: int):
    delete_keys_containing(user_id)