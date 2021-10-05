import random
from typing import List, Dict
import math
import numpy as np


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    # print(f'my_head:{my_head}, my_body:{my_body}')
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
    # print(f'in avoid_border, board_height:{board_height}, board_width:{board_width}, my_head:{my_head}')
    if board_height - 1 == my_head["y"] and 'up' in possible_moves:
        possible_moves.remove("up")
        # print('remove up')
    if 0 == my_head["y"] and 'down' in possible_moves:
        possible_moves.remove("down")
        # print('remove down')
    if board_width - 1 == my_head["x"] and 'right' in possible_moves:
        possible_moves.remove("right")
        # print('remove right')
    if 0 == my_head["x"] and 'left' in possible_moves:
        possible_moves.remove("left")
        # print('remove left')
    return possible_moves


def get_foods_sorted_by_distance_asc(my_head: Dict[str, int], foods: List[dict]):
    # print(f'my_head:{my_head}, foods:{foods}')
    length_food_list = []
    for food in foods:
        # print(f'food:{food}, my_head:{my_head}')
        distance = math.sqrt((food['x'] - my_head['x']) ** 2 + (food['y'] - my_head['y']) ** 2)
        length_food_list.append({'distance': distance, 'food': food})
    length_food_list_sorted = sorted(length_food_list, key=lambda x: x['distance'])
    food_list_sorted = list(map(lambda x: x['food'], length_food_list_sorted))
    return food_list_sorted


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
    not_accessible_tiles = my_body[:-1]
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


def possible_move_to_index(possible_move: str, my_head: Dict[str, int]):
    if possible_move == 'up':
        return {"x": my_head["x"], "y": my_head["y"] + 1}
    if possible_move == 'down':
        return {"x": my_head["x"], "y": my_head["y"] - 1}
    if possible_move == 'right':
        return {"x": my_head["x"] + 1, "y": my_head["y"]}
    if possible_move == 'left':
        return {"x": my_head["x"] - 1, "y": my_head["y"]}


def re_prioritize_preferred_directions_based_on_free_connected_tile(my_head: Dict[str, int], my_body: List[dict], other_snakes: List[dict], board_height: int, board_width: int, possible_moves_prioritized: List[str]):
    result_list = []
    for move in possible_moves_prioritized:
        possible_move_index = possible_move_to_index(move, my_head)
        number_of_connected_tile = get_number_of_connected_tile(possible_move_index, my_body, other_snakes, board_height, board_width)
        # print(f'number_of_connected_tile:{number_of_connected_tile}')
        result_list.append({'move': move, 'number_of_connected_tile': number_of_connected_tile})
    # print(f'result_list:{result_list}')
    result_list = sorted(result_list, key=lambda x: x['number_of_connected_tile'], reverse=True)
    # print(f'result_list:{result_list}')
    result_list = list(map(lambda x: x['move'], result_list))
    return result_list


def populate_min_step_to_reach_matrix(min_step_to_reach_matrix: List[List[int]], not_accessible_tiles: List[dict], processed_tiles: List[dict], board_height: int, board_width: int, from_tile: Dict[str, int], to_tile: Dict[str, int], target_tile: Dict[str, int]):
    # print(f'in populate_min_step_to_reach_matrix:from_tile:{from_tile}, to_tile:{to_tile}')
    if to_tile in not_accessible_tiles:
        return
    if to_tile in processed_tiles:
        return
    if to_tile == target_tile:
        return
    if from_tile['x'] == board_width or from_tile['x'] == -1:
        return
    if from_tile['y'] == board_height or from_tile['y'] == -1:
        return
    if to_tile['x'] == board_width or to_tile['x'] == -1:
        return
    if to_tile['y'] == board_height or to_tile['y'] == -1:
        return
    old_value = min_step_to_reach_matrix[to_tile['x']][to_tile['y']]
    new_value = min_step_to_reach_matrix[from_tile['x']][from_tile['y']] + 1
    if old_value == '-':
        min_step_to_reach_matrix[to_tile['x']][to_tile['y']] = new_value
    else:
        min_step_to_reach_matrix[to_tile['x']][to_tile['y']] = min(old_value, new_value)
    processed_tiles.append(to_tile)
    # print(f'update ({to_tile["x"]},{to_tile["y"]}) = {min_step_to_reach_matrix[to_tile["x"]][to_tile["y"]]}, processed_tiles={processed_tiles}')
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, processed_tiles, board_height, board_width, to_tile, {"x": to_tile["x"] + 1, "y": to_tile["y"]}, target_tile)
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, processed_tiles, board_height, board_width, to_tile, {"x": to_tile["x"], "y": to_tile["y"] + 1}, target_tile)
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, processed_tiles, board_height, board_width, to_tile, {"x": to_tile["x"] - 1, "y": to_tile["y"]}, target_tile)
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, processed_tiles, board_height, board_width, to_tile, {"x": to_tile["x"], "y": to_tile["y"] - 1}, target_tile)
    # # DEBUG
    # print('-------------------------------------------------')
    # print_min_step_to_reach_matrix(min_step_to_reach_matrix)
    # print('-------------------------------------------------')


def print_min_step_to_reach_matrix(min_step_to_reach_matrix: List[List[int]]):
    height = len(min_step_to_reach_matrix)
    for i in range(height):
        print(min_step_to_reach_matrix[height - i - 1])


def get_paths_to_foods(data: dict):
    board_height = data['board']['height']
    board_width = data['board']['width']
    foods = data['board']['food']
    head = data["you"]["head"]
    body = data["you"]["body"]
    other_snakes = data['board']['snakes']
    foods = get_foods_sorted_by_distance_asc(head, data['board']['food'])
    selected_food = foods[0]
    #
    not_accessible_tiles = body[:-1]
    for other_snake in other_snakes:
        not_accessible_tiles = not_accessible_tiles + other_snake['body']
    # max = board_height * board_width
    min_step_to_reach_matrix = [['-' for x in range(board_width)] for y in range(board_height)]
    min_step_to_reach_matrix[head['x']][head['y']] = 0
    min_step_to_reach_matrix[selected_food['x']][selected_food['y']] = -1
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, [head], board_height, board_width, head, {"x": head["x"] + 1, "y": head["y"]}, selected_food)  ############# CONSIDER OTHER FOOD
    print_min_step_to_reach_matrix(min_step_to_reach_matrix)
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, [head], board_height, board_width, head, {"x": head["x"], "y": head["y"] + 1}, selected_food)  ############# CONSIDER OTHER FOOD
    print_min_step_to_reach_matrix(min_step_to_reach_matrix)
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, [head], board_height, board_width, head, {"x": head["x"] - 1, "y": head["y"]}, selected_food)  ############# CONSIDER OTHER FOOD
    print_min_step_to_reach_matrix(min_step_to_reach_matrix)
    populate_min_step_to_reach_matrix(min_step_to_reach_matrix, not_accessible_tiles, [head], board_height, board_width, head, {"x": head["x"], "y": head["y"] - 1}, selected_food)  ############# CONSIDER OTHER FOOD
    # DEBUG
    # print('-------------------------------------------------')
    # print(f'body:{body}, foods:{foods}')
    # print_min_step_to_reach_matrix(min_step_to_reach_matrix)
    # print('-------------------------------------------------')


def choose_move(data: dict) -> str:
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
        nearest_food = get_foods_sorted_by_distance_asc(my_head, data['board']['food'])[0]
        print(f'nearest_food:{nearest_food}')
        possible_moves_prioritized = get_preferred_directions_to_food(my_head, nearest_food, possible_moves)
        print(f'possible_moves_prioritized based on food:{possible_moves_prioritized}')
        possible_moves_prioritized = re_prioritize_preferred_directions_based_on_free_connected_tile(my_head, my_body, data['board']['snakes'], data['board']['height'], data['board']['width'], possible_moves_prioritized)
        print(f'possible_moves_prioritized based on free connected tile:{possible_moves_prioritized}')
    print(f'possible_moves_prioritized:{possible_moves_prioritized}')
    # debug start
    get_paths_to_foods(data)
    # debug end
    move = possible_moves_prioritized[0]
    print(f'possible_moves_prioritized:{possible_moves_prioritized}')
    print(
        f"=======> {data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves_prioritized}"
    )
    return move
