import json
import sys
import logging
import random

import consts
if consts.TYPECHECK:
    from level import Level

def get_plant_costs():
    cost_dict = {}
    with open(consts.PLANT_STATS_FILE_PATH, "r") as plant_stats_file:
        plant_stats_dict = json.load(plant_stats_file)
    for plant, stats in plant_stats_dict.items():
        cost_dict[plant] = stats["cost"]
    return cost_dict

def get_plant_names():
    with open(consts.PLANT_STATS_FILE_PATH, "r") as plant_stats_file:
        plant_stats_dict = json.load(plant_stats_file)
    return plant_stats_dict.keys()

def get_zombies_to_be_spawned(level_data: dict) -> dict:
    zombies_to_be_spawned = dict()
    for key, value in level_data.items():
        if not key.isnumeric():
            continue
        zombies_to_be_spawned[key] = value
    return zombies_to_be_spawned

def configure_logging(logfile: str):
    if consts.LOGS_TO_STDERR:
        logging.basicConfig(stream=sys.stderr, level=consts.LOG_LEVEL, format=consts.LOG_FORMAT)
    else:
        logging.basicConfig(level=consts.LOG_LEVEL, format=consts.LOG_FORMAT)
        logger = logging.getLogger()
        new_file_handler = logging.FileHandler(logfile)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(new_file_handler)

def printable_grid(level: "Level"):
    height = level.lanes
    length = level.columns
    grid = [[0 for _ in range(length)] for _ in range(height)]
    for x in range(height):
        for y in range(length):
            if level.plant_grid[x][y]:
                grid[x][y] = 1
            if level.zombie_grid[x][y]:
                grid[x][y] += 100
    for bullet in level.bullets:
        x, y = bullet.lane, bullet.column
        grid[x][y] += 10
    for x in range(height):
        for y in range(length):
            num_in_grid = grid[x][y]
            to_write_in_grid = ""
            if num_in_grid % 10 == 1: # there is a plant there
                to_write_in_grid = 'P'
            else:
                to_write_in_grid = '_'
            if (num_in_grid // 10) % 10 >= 1:
                to_write_in_grid += 'B'
            else:
                to_write_in_grid += '_'
            if (num_in_grid // 100) % 10 == 1:
                to_write_in_grid += 'Z'
            else:
                to_write_in_grid += '_'
            grid[x][y] = to_write_in_grid
    for x in range(height):
        if level.home_column[x]:
            grid[x] = ["M"] + grid[x]
        else:
            grid[x] = ["_"] + grid[x]
    return grid

def generate_random_level_dict(lanes, difficulty="easy"):
    diff_set = consts.difficulty[difficulty]
    level_dict = {}
    time = random.randrange(diff_set["first_spawn_low"], diff_set["first_spawn_high"] + 1)
    for _ in range(diff_set["waves"]):
        num_of_zombies = random.randrange(diff_set["num_of_zombies_low"], diff_set["num_of_zombies_high"] + 1)
        level_dict[str(time)] = []
        for _ in range(num_of_zombies):
            zombie_spawn = [random.choices(diff_set["zombie_types"], weights=diff_set["zombie_weights"], k=1)[0], random.randrange(0, lanes)]
            level_dict[str(time)].append(zombie_spawn)
        time += random.randrange(diff_set["spawn_interval_low"], diff_set["spawn_interval_high"] + 1)

    with open("resources/random_level.json", "w") as random_level_file:
        json.dump(level_dict, random_level_file)

    return level_dict