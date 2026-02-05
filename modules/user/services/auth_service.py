from dependencies.redis_client import delete_keys_containing, get_client
from fastapi import Response, status
from dependencies.token_service import create_tokens
from modules.user.dtos.openid_dto import OpenIDDTO
from dependencies.token_service import check_token
import os, httpx, secrets, redis
from dotenv import load_dotenv
from utils.state_generator import create_state
from utils.pkce_code_utils import code_verifier, code_challenge
from modules.user.services.user_service import (
    create_in_db,
    save_in_redis
)

load_dotenv()

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SERVICE")
redirect_uri = os.getenv("CALLBACK_URL")
spotify_user_endpoint = "https://api.spotify.com/v1/me"
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
            "code_challenge": code_chall,
            "show_dialog": "true"
        }
    
    return (
        spotify_auth_url,
        params
    )

async def exchange_code_token(code: str, state: str):
    '''
    Exchange auth code for Spotify access and refresh tokens
    
    :param code: auth code from Spotify Response
    :type code: str
    :param state: state string from Spotify Response
    :type state: str

    '''
    verifier = get_code(state)
    # i need to add guards here (try/catch)
    async with httpx.AsyncClient() as client:
        response = await client.post(
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
    openid = fetch_user_info(response.json()["access_token"])
    sid = gen_sid()
    save_user_and_tokens(
        sid,
        openid,
        response.json()["access_token"],
        response.json()["refresh_token"]
    )
    return sid

def fetch_user_info(spotify_access_token: str) -> OpenIDDTO:
    '''
    Fetch user info from Spotify API endpoint
    '''
    # also add guards here
    with httpx.Client() as client:
        r = client.get(
            url=spotify_user_endpoint,
            headers={
                "Authorization" : f"Bearer {spotify_access_token}"
            }
        )
    print("Response:", r.status_code, r.text)
    return OpenIDDTO(
        username=r.json()["id"],
        email=r.json()["email"],
        display_name=r.json()["display_name"]
    )

def save_user_and_tokens(
        sid: str,
        user: OpenIDDTO,
        spotify_access_token: str,
        spotify_refresh_token: str
        ) -> str:
    user_db = create_in_db(user)
    # create backend tokens
    app_access_token, app_refresh_token = create_tokens(user_db.model_dump())
    # print(f"Test ------------- {app_access_token}")
    # print(f"Test ------------- {app_refresh_token}")
    # save all tokens in redis
    if app_access_token and app_refresh_token:
        save_in_redis(
            sid,
            user_db.id,
            app_access_token,
            app_refresh_token,
            spotify_access_token,
            spotify_refresh_token
            )
    return sid

def check_auth(
        r: redis.Redis, 
        sid: str
        ):
    sid=sid[4:]
    if not r.exists(f"session:{sid}"):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    

    token = r.hget(f"session:{sid}", "access_token")
    # wont need this bc we only need to check the session, and we no longer have a jwt in header although i could leave the check just for support
    check_token(token, r, sid)





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

def delete_session():
    r = get_client()
    r.delete(f"code:*")

def logout_service(user_id: int):
    delete_keys_containing(user_id)

def gen_sid():
    return secrets.token_urlsafe(32)