from modules.game.dtos.clean_retrieval import AnimeRedis
from modules.game.dtos.game_room_dto import GameRoom, Guess
from dependencies.redis_client import get_client
from fastapi import Response
from fastapi.responses import JSONResponse
import random
'''
Game logic.
'''
r = get_client()


def find_game_room(player_id: int):
    resulting_tuple = r.scan(match="game_room:*")
    if resulting_tuple and resulting_tuple[1]:
        # print(resulting_tuple[1])
        player_ids = r.json().mget(resulting_tuple[1], "$.players.*.id")
        if player_ids:
            # print(player_id)
            # print(player_ids)
            flattened = sum(player_ids, [])
            # print(flattened)
            if player_id in flattened: 
                game_room_key = resulting_tuple[1][0]
                return game_room_key
            else:
                return None
        
def selection(player_id: int):
    '''
    Returns: (anime_titles, game_room_key, status)
    status can be: "success", "game_over", "no_room", "no_anime"
    '''
    game_room_key = find_game_room(player_id)
    
    if not game_room_key:
        return None, None, "no_room"
    
    anime_count = r.json().arrlen(game_room_key, "$.anime_list")
    if anime_count[0] == 0:
        scoreboard = r.json().get(game_room_key, "$.scoreboard")[0]
        r.json().delete(game_room_key, "$")
        return scoreboard, game_room_key, "game_over"
    
    random_selection = random.randint(0, anime_count[0] - 1)
    selected_anime = r.json().get(game_room_key, f"$.anime_list[{random_selection}]")
    r.json().delete(game_room_key, f"$.anime_list[{random_selection}]")

    if not selected_anime[0]["titles"]:
        return None, game_room_key, "no_anime"
    
    return selected_anime[0]["titles"], game_room_key, "success"


def guessing(guess: Guess, player_id: int):
    if not guess:
        return {"error": "Player did not submit a guess"}
    
    response, game_room_key, status = selection(player_id)
    
    if status == "no_room":
        return {"error": "Game room not found"}
    elif status == "game_over":
        return {"message": "Game Over!",
                "scoreboard": response
                }
    elif status == "no_anime":
        return {"error": "No valid anime found"}
    
    r.json().numincrby(game_room_key, "$.scoreboard.rounds", -1)
    for title in response:
        if title["name"].lower() == guess.name.lower():
            r.json().numincrby(game_room_key, f"$.scoreboard.players_scores.{player_id}", 1)
            scoreboard = r.json().get(game_room_key, "$.scoreboard.players_scores")
            
            return {
                "result": "Correct!",
                "scoreboard": scoreboard[0] if scoreboard else {}
            }
    
    scoreboard = r.json().get(game_room_key, "$.scoreboard.players_scores")
    return {
        "result": "Wrong!",
        "scoreboard": scoreboard[0] if scoreboard else {},
        "rounds_left": r.json().get(game_room_key, "$.scoreboard.rounds")[0]
    }

def get_scoreboard(player_id: int):
    '''return scoreboard'''
    game_room_key = find_game_room(player_id)
    if game_room_key:
        return r.json().get(game_room_key, "$.scoreboard")[0]