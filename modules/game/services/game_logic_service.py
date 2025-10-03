from db.session_manager import get_db
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from modules.game.dtos.clean_retrieval import AnimeRedis
from modules.game.dtos.game_room_dto import GameRoom
from dependencies.redis_client import get_client
from typing import List
import uuid, random
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

    '''
    alright so current situation is that we can successfully fetch the elements of each game room. Now we need to just extract the animes to pick from. I wonder if there is a way for us to only get the player's id rather than all the information inside the game room obj??
    I dont think we can do it with mget and mget seems to be the most convenient method to retrieve the contents of the game rooms so im just going to run with this implementation but i believe it could be optimized if i spent more time on it.


    ok so i validate the game room objects so i could get type checking and dot notation access. Now i just need to get the attributes.
    '''
    anime_titles = []
    for room in validated_game_room_contents:
        for attributes in room.anime_list:
            # print(attributes.openings)
            # print(attributes.endings)
            # print(attributes.titles)
            anime_titles.extend(attributes.titles)

    return anime_titles
    '''
    ok now we have the attributes. technically now i would pass the name of the song to my client so it could play the song in a react frontend but i dont have that yet so we are going to pretend i did that and the user is going to guess now.
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