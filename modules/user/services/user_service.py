# import httpx, base64
from modules.user.dtos.user_create_dto import UserCreateDTO
from modules.user.models.user_models import UserORM
from db.session_manager import get_db
# from dependencies.spotify_sso import (
#     redirect_uri,
#     client_id,
#     client_secret
# )


def create(user: UserCreateDTO) -> None:
    db_gen = get_db()  # this is a generator
    db = next(db_gen)  # this gets the actual session instance
    
    query = db.query(UserORM).filter(
        UserORM.email == user.email,
        UserORM.username == user.id 
    ).first()

    if not query:
        user_orm = UserORM(
            username=user.id,  
            email=user.email,
            display_name=user.display_name
        )
        db.add(user_orm)
        db.commit()
        
        
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