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

# def selection(room_id: str):
#     # Get the anime list length first
#     anime_count = r.json().arrlen(f"game_room:{room_id}", "$.anime_list")[0]
    
#     if anime_count == 0:
#         return None  # Game over
    
#     # Select random index
#     random_selection = random.randint(0, anime_count - 1)
    
#     # Get the selected anime
#     selected_anime = r.json().get(f"game_room:{room_id}", f"$.anime_list[{random_selection}]")[0]
    
#     # Remove it from the list
#     r.json().delete(f"game_room:{room_id}", f"$.anime_list[{random_selection}]")
    
#     return selected_anime

def selection(player_id: int):
    '''
    1. select a random anime from the available animes in the game_room object.
    2. when an anime is selected, delete it from the game_room object
    3. Once there are no more animes, game is over, and return the scoreboard
    '''
    resulting_tuple = r.scan(match="game_room:*")
    if resulting_tuple:
        # print(resulting_tuple[1])
        player_ids = r.json().mget(resulting_tuple[1], "$.players.*.id")
        # print(player_id)
        # print(player_ids)
        flattened = sum(player_ids, [])
        # print(flattened)
        game_room_key = resulting_tuple[1][0]
        if player_id in flattened:
            anime_count = r.json().arrlen(game_room_key, "$.anime_list")
            # print(f"found it: {anime_count}")
            print(game_room_key)
            random_selection = random.randint(0,anime_count[0]) # the limit should be the size of the anime list
            if random_selection:
                selected_anime: AnimeRedis = r.json().get(game_room_key, f"$.anime_list[{random_selection}]")
                # print(selected_anime[0]["titles"]) #come back to this

    r.json().delete(game_room_key, f"$.anime_list[{random_selection}]")
    return selected_anime[0]["titles"]


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