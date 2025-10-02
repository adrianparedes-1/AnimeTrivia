from db.session_manager import get_db
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from modules.game.dtos.clean_retrieval import CleanList
from modules.anime.models.anime_orm_model import Anime
from dependencies.redis_client import get_client
from typing import List
import uuid, random
'''
Game logic.
'''
r = get_client()



def selection():
    '''
    1. select a random anime from the available animes in the game_room object.
    2. when an anime is selected, delete it from the game_room object
    3. Once there are no more animes, game is over, and return the scoreboard
    '''
    ...
    '''
    fetching the current game object could be bit complicated bc we have to consider if there are multiple game rooms running at the same time, we have to look inside the game room obj and check the players.
    players can only be in 1 game room at a time so the first instance of the player should be the correct one.
    '''
    


def guessing():
    '''
    1. player sends guess
    '''
    ...


def guess_check():
    '''
    check the player's guess vs. the selected anime
    '''
    ...


def scoreboard():
    '''
    1. update the player's score
    2. return the player's current score
    '''
    ...