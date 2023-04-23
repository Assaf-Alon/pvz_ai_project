import json

import consts
# from level import Level

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


def printable_grid(level: "Level"):
    height = level.height
    length = level.length
    grid = [[0 for _ in range(length)] for _ in range(height)]
    for x in range(height):
        for y in range(length):
            if level.plant_grid[x][y]:
                grid[x][y] = 1
            if level.zombie_grid[x][y]:
                grid[x][y] += 100
    for bullet in level.bullets:
        x, y = bullet.position
        grid[x][y] += 10
    for x in range(height):
        for y in range(length):
            num_in_grid = grid[x][y]
            to_write_in_grid = ""
            if num_in_grid % 10 == 1: # there is a plant there
                to_write_in_grid = 'P'
            else:
                to_write_in_grid = '_'
            if (num_in_grid // 10) % 10 == 1:
                to_write_in_grid += 'B'
            else:
                to_write_in_grid += '_'
            if (num_in_grid // 100) % 10 == 1:
                to_write_in_grid += 'Z'
            else:
                to_write_in_grid += '_'
            grid[x][y] = to_write_in_grid
    return grid