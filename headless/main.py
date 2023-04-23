import json
import time
import level
from pprint import pprint
import os
from copy import deepcopy
from utils import printable_grid
    # def __init__(self, length, height, level_data: dict, random = False, fps = 30):

if __name__ == "__main__":
    with open("resources/level0.json", "r") as level_data_file:
        level_data = json.load(level_data_file)
    env = level.Level(10, 5, level_data, False, fps=10)
    while not env.done:
        env.step("")
        # env.print_grid()
        printable_zombie_grid = printable_grid(env)
        pprint(printable_zombie_grid)
        print(f"frame num: {env.frame}")
        for zombie in env.zombies:
            print(zombie.pos)
        
        time.sleep(0.1)
        os.system('clear')
        if (env.frame >= 20):
            x = 0
            # breakpoint?