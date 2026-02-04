# import httpx, base64
from modules.user.dtos.openid_dto import OpenIDDTO
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


# def fetch_user_id():
#     '''
#     Fetch user id from db
#     '''
#     with next(get_db(request)) as db:
#         query = db.query(User).filter(
#             User.id == user_id
#         ).first()

def create_in_db(user: OpenIDDTO) -> UserAuthResponse:
    with next(get_db()) as db:
        query_existing = db.query(User).filter(
            User.email == user.email,
            User.username == user.username
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
                raise # since we will be rolling back, we need to let the error handler know that there was an issue, so we raise an error with the traceback
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


def save_in_redis(
        sid: str,
        user_id: int, 
        app_access_token: str,
        app_refresh_token: str,
        spotify_access_token: str,
        spotify_refresh_token: str
        ):
    r = get_client()
    # i need to set these individually for separate expiration timers
    r.setex(f"{sid}:{user_id}:app_access_token", 86400, app_access_token) # for development 
    r.setex(f"{sid}:{user_id}:app_refresh_token", 86400, app_refresh_token)
    r.setex(f"{sid}:{user_id}:spotify_access_token", 3600, spotify_access_token)
    r.setex(f"{sid}:{user_id}:spotify_refresh_token", 86400, spotify_refresh_token)

    # uncomment to print values
    # keys = r.keys(f"{user_id}:*")
    # for key in keys:
    #     value = r.get(key)
    #     print(f"{key} => {value}")


