# import httpx, base64
from modules.user.dtos.user_create_dto import UserCreateDTO
from modules.user.dtos.user_response_dto import UserAuthResponse
from modules.user.models.user_model import User
from modules.menu.models.profile_model import Profile
from db.session_manager import get_db
from dependencies.redis_client import get_client
# from dependencies.spotify_sso import (
#     redirect_uri,
#     client_id,
#     client_secret
# )


def create(user: UserCreateDTO) -> UserAuthResponse:
    with next(get_db()) as db:
        query_existing = db.query(User).filter(
            User.email == user.email,
            User.username == user.id
        ).first()

        if not query_existing:
            user_orm = User(
                username=user.id,
                email=user.email,
                display_name=user.display_name
            )
            profile_orm = Profile(
                username=user.id,
                email=user.email,
                display_name=user.display_name,
                user=user_orm
            )
            db.add_all(instances=[user_orm, profile_orm])
            try:
                db.commit() # commit to db
            except Exception:
                db.rollback() # if there is any issue, rollback to clean state
                raise # since we will be rolling back, we need to let the error handler that there was an issue, so we raise an error with the traceback
            db.refresh(user_orm)
            user_db = user_orm
        else:
            user_db = query_existing

        # convert to dto
        return UserAuthResponse(
            id=user_db.id,
            username=user_db.username,
            email=user_db.email,
            display_name=user_db.display_name
        )


def save_in_redis(user_id, 
            app_access_token,
            app_refresh_token,
            spotify_access_token,
            spotify_refresh_token
            ):
    r = get_client()
    r.setex(f"{user_id}:app_access_token", 3600, app_access_token)
    r.setex(f"{user_id}:app_refresh_token", 86400, app_refresh_token)
    r.setex(f"{user_id}:spotify_access_token", 3600, spotify_access_token)
    r.setex(f"{user_id}:spotify_refresh_token", 86400, spotify_refresh_token)

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