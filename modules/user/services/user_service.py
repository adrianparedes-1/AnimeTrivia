# import httpx, base64
from modules.user.dtos.user_create_dto import UserCreateDTO
from modules.user.models.user_model import UserORM
from db.session_manager import get_db
import redis
# from dependencies.spotify_sso import (
#     redirect_uri,
#     client_id,
#     client_secret
# )


def create(user: UserCreateDTO) -> UserORM:
    db_gen = get_db()  # this is a generator
    db = next(db_gen)  # this gets the actual session instance
    
    
    user_db = db.query(UserORM).filter(
        UserORM.email == user.email,
        UserORM.username == user.id
    ).first()

    if not user_db:
        user_db = UserORM(
            username=user.id,
            email=user.email,
            display_name=user.display_name
        )
        db.add(user_db)
        db.commit()
        db.refresh(user_db)  # ensures user_db has up-to-date info from DB
    
    print(user_db)

    return user_db

def save_in_redis(user_id: str, 
            app_access_token,
            app_refresh_token,
            spotify_access_token,
            spotify_refresh_token
            ):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.setex(f"{user_id}:app_access_token:", 3600, app_access_token)
    r.setex(f"{user_id}:app_refresh_token:", 86400, app_refresh_token)
    r.setex(f"{user_id}:spotify_access_token:", 3600, spotify_access_token)
    r.setex(f"{user_id}:spotify_refresh_token:", 86400, spotify_refresh_token)

    # uncomment to print values
    # keys = r.keys(f"{user_id}:*")
    # for key in keys:
    #     value = r.get(key)
    #     print(f"{key} => {value}")

# async def exchange_code_token(code: str):
#     async with httpx.AsyncClient() as client:
#         r = await client.post("https://accounts.spotify.com/api/token",
#                           headers={
#                               "Authorization" : f"Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}",
#                               "Content-Type" : "application/x-www-form-urlencoded"
#                               },
#                           data={
#                               "grant_type": "authorization_code",
#                               "code" : f"{code}",
#                               "redirect_uri" : f"{redirect_uri}"
#                           })
    
#     return r