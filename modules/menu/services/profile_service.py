'''
We will search for the player info and history based off the player id provided.
There should probably be a uuid for the player which we can pass rather than passing the username in redis
'''

from modules.menu.dtos.player_profile_dto import PlayerProfileDTO
from modules.menu.models.profile_model import Profile
from db.session_manager import get_db


def show_profile(profile) -> PlayerProfileDTO:
    db_gen = get_db()  # this is a generator
    db = next(db_gen)  # this gets the actual session instance
    user_profile = db.query(Profile).filter(
        Profile.email == profile["email"],
        Profile.username == profile["username"] # workaround for now but will go back to id
    ).first()

    if not user_profile:
        return "profile not found"
    
    return user_profile