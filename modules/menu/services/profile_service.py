'''
We will search for the player info and history based off the player id provided.
There should probably be a uuid for the player which we can pass rather than passing the username in redis
'''

from modules.menu.dtos.player_profile_dto import PlayerProfileDTO
# from modules.user.models.user_model import UserORM
from db.session_manager import get_db


def show_profile(profile: PlayerProfileDTO) -> None:
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