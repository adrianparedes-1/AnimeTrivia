from db.session_manager import get_db
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from modules.game.dtos.clean_retrieval import AnimeRedis
from modules.game.dtos.game_room_dto import GameRoom, Guess
from dependencies.redis_client import get_client
from typing import List
import random
'''
Game logic.
'''
r = get_client()

keys_index = 1

def selection():
    '''
    1. select a random anime from the available animes in the game_room object.
    2. when an anime is selected, delete it from the game_room object
    3. Once there are no more animes, game is over, and return the scoreboard
    '''
    ...
    resulting_tuple = r.scan(match="game_room:*")
    
    if resulting_tuple:
        list_conversion = []
        list_conversion.extend(resulting_tuple)
        list_conversion = list_conversion[keys_index]
        game_room_contents = r.json().mget(list_conversion, "$")

        validated_game_room_contents: List[GameRoom] = []
        for room in game_room_contents:
            validated_game_room_contents.append(GameRoom.model_validate(room[0]))

    for room in validated_game_room_contents:
        random_selection = random.randint(0,9)
        random_anime = room.anime_list[random_selection]
    print(random_anime)
    r.json().delete(random_anime.anime, f"{resulting_tuple}")
    return random_anime.titles


def guessing(guess: Guess):
    '''
    1. player sends guess.

    Player will guess by sending a string with the anime name in the body of a POST request
    '''
    if guess:
        anime_titles = selection()
        for title in anime_titles:
            if title.name == guess.name:
                return 'CORRECT!' #should be returning the player's updated score
        return 'WRONG!'
    else:
        return "Player did not submit a guess"

def scoreboard():
    '''
    1. update the player's score
    2. return the player's current score
    '''
    ...