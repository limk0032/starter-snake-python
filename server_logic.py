import random
from typing import List, Dict
import math

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    print(f'my_head:{my_head}, my_body:{my_body}')
    if {"x": my_head["x"], "y": my_head["y"] + 1} in my_body and 'up' in possible_moves:
        possible_moves.remove("up")
    if {"x": my_head["x"], "y": my_head["y"] - 1} in my_body and 'down' in possible_moves:
        possible_moves.remove("down")
    if {"x": my_head["x"] + 1, "y": my_head["y"]} in my_body and 'right' in possible_moves:
        possible_moves.remove("right")
    if {"x": my_head["x"] - 1, "y": my_head["y"]} in my_body and 'left' in possible_moves:
        possible_moves.remove("left")
    return possible_moves


def avoid_border(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str], board_height: int, board_width: int) -> List[str]:
    print(f'in avoid_border, board_height:{board_height}, board_width:{board_width}, my_head:{my_head}')
    if board_height - 1 == my_head["y"] and 'up' in possible_moves:
        possible_moves.remove("up")
        print('remove up')
    if 0 == my_head["y"] and 'down' in possible_moves:
        possible_moves.remove("down")
        print('remove down')
    if board_width - 1 == my_head["x"] and 'right' in possible_moves:
        possible_moves.remove("right")
        print('remove right')
    if 0 == my_head["x"] and 'left' in possible_moves:
        possible_moves.remove("left")
        print('remove left')
    return possible_moves


def get_nearest_food(my_head: Dict[str, int], foods: List[dict]):
    print(f'my_head:{my_head}, foods:{foods}')
    length_food_dict = {}
    for food in foods:
        distance = math.sqrt((food['x'] - my_head['x']) ** 2 + (food['y'] - my_head['y']) ** 2)
        length_food_dict[distance] = food
    length_list = length_food_dict.keys()
    min_length = min(length_list)
    return length_food_dict[min_length]


def combine_preferred_directions_with_possible_moves(preferred_directions: List[str], possible_moves: List[str]):
    result = []
    for preferred_direction in preferred_directions:
        if preferred_direction in possible_moves:
            result.append(preferred_direction)
    return result


def get_preferred_directions_to_food(my_head: Dict[str, int], food: Dict[str, int], possible_moves: List[str]):
    preferred_direction = []
    if food['x'] == my_head['x'] and food['y'] < my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['down', 'left', 'right', 'up'], possible_moves)
    elif food['x'] == my_head['x'] and food['y'] > my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['up', 'left', 'right', 'down'], possible_moves)
    elif food['x'] < my_head['x'] and food['y'] == my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['left', 'up', 'down', 'right'], possible_moves)
    elif food['x'] > my_head['x'] and food['y'] == my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['right', 'up', 'down', 'left'], possible_moves)
    elif food['x'] < my_head['x'] and food['y'] < my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['down', 'left', 'up', 'right'], possible_moves)
    elif food['x'] < my_head['x'] and food['y'] > my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['up', 'left', 'down', 'right'], possible_moves)
    elif food['x'] > my_head['x'] and food['y'] < my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['down', 'right', 'up', 'left'], possible_moves)
    elif food['x'] > my_head['x'] and food['y'] > my_head['y']:
        preferred_direction = combine_preferred_directions_with_possible_moves(['up', 'right', 'down', 'left'], possible_moves)
    return preferred_direction


def get_number_of_connected_tile(start: Dict[str, int], my_body: List[dict], other_snakes: List[List[dict]], board_height: int, board_width: int):
    processed_tiles = []
    not_accessible_tiles = my_body
    for other_snake in other_snakes:
        not_accessible_tiles = not_accessible_tiles + other_snake['body']
    number_of_connected_tile = get_number_of_connected_tile_recursively(start, not_accessible_tiles, board_height, board_width, processed_tiles)
    return number_of_connected_tile


def get_number_of_connected_tile_recursively(start: Dict[str, int], not_accessible_tiles: List[dict], board_height: int, board_width: int, processed_tiles: List[dict]):
    if start in processed_tiles:
        return 0
    if start in not_accessible_tiles:
        return 0
    if start['x'] < 0 or start['x'] == board_width:
        return 0
    if start['y'] < 0 or start['y'] == board_height:
        return 0
    processed_tiles.append(start)
    result = 1
    result = result + get_number_of_connected_tile_recursively({"x": start["x"] + 1, "y": start["y"]}, not_accessible_tiles, board_height, board_width, processed_tiles)
    result = result + get_number_of_connected_tile_recursively({"x": start["x"], "y": start["y"] + 1}, not_accessible_tiles, board_height, board_width, processed_tiles)
    result = result + get_number_of_connected_tile_recursively({"x": start["x"] - 1, "y": start["y"]}, not_accessible_tiles, board_height, board_width, processed_tiles)
    result = result + get_number_of_connected_tile_recursively({"x": start["x"], "y": start["y"] - 1}, not_accessible_tiles, board_height, board_width, processed_tiles)
    return result


def posible_move_to_index(possible_move: str, my_head: Dict[str, int]):
    if possible_move == 'up':
        return {"x": my_head["x"], "y": my_head["y"] + 1}
    if possible_move == 'down':
        return {"x": my_head["x"], "y": my_head["y"] - 1}
    if possible_move == 'right':
        return {"x": my_head["x"] + 1, "y": my_head["y"]}
    if possible_move == 'left':
        return {"x": my_head["x"] - 1, "y": my_head["y"]}


def repriotize_preferred_directions_based_on_free_connected_tile(my_head: Dict[str, int], my_body: List[dict], other_snakes: List[dict], board_height: int, board_width: int, possible_moves_priotized: List[str]):
    result_list = []
    for move in possible_moves_priotized:
        posible_move_index = posible_move_to_index(move, my_head)
        number_of_connected_tile = get_number_of_connected_tile(posible_move_index, my_body, other_snakes, board_height, board_width)
        print(f'number_of_connected_tile:{number_of_connected_tile}')
        result_list.append({'move': move, 'number_of_connected_tile': number_of_connected_tile})
    print(f'result_list:{result_list}')
    result_list = sorted(result_list, key=lambda x: x['number_of_connected_tile'], reverse=True)
    print(f'result_list:{result_list}')
    result_list = list(map(lambda x: x['move'], result_list))
    return result_list


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]
    my_body = data["you"]["body"]

    possible_moves = ["up", "down", "left", "right"]

    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    possible_moves = avoid_border(my_head, my_body, possible_moves, data['board']['height'], data['board']['width'])
    if data['board']['snakes']:
        for snake in data['board']['snakes']:
            possible_moves = avoid_my_neck(my_head, snake['body'], possible_moves)

    print(f'possible_moves:{possible_moves}')
    if data['board']['food']:
        print('food on board found')
        nearest_food = get_nearest_food(my_head, data['board']['food'])
        print(f'nearest_food:{nearest_food}')
        possible_moves_priotized = get_preferred_directions_to_food(my_head, nearest_food, possible_moves)
        print(f'possible_moves_priotized based on food:{possible_moves_priotized}')
        possible_moves_priotized = repriotize_preferred_directions_based_on_free_connected_tile(my_head, my_body, data['board']['snakes'], data['board']['height'], data['board']['width'], possible_moves_priotized)
        print(f'possible_moves_priotized based on free connectedtile:{possible_moves_priotized}')
    move = possible_moves_priotized[0]

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves_priotized}"
    )

    return move
