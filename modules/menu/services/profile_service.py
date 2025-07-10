'''
We will search for the player info and history based off the player id provided.
There should probably be a uuid for the player which we can pass rather than passing the username in redis
'''

from modules.menu.dtos.player_profile_dto import PlayerProfileDTO
from modules.user.models.user_model import UserORM
from db.session_manager import get_db


def show_profile(profile) -> PlayerProfileDTO:
    db_gen = get_db()  # this is a generator
    db = next(db_gen)  # this gets the actual session instance
    print(profile)
    # query = db.query(UserORM).filter(
    #     UserORM.username == profile.id
    # ).first()

    # if not query:
    #     return "user not found"
    
    return profile