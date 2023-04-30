import json
import sys
import logging
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
        if level.lawnmowers[x]:
            grid[x] = ["M"] + grid[x]
        else:
            grid[x] = ["_"] + grid[x]
    return grid