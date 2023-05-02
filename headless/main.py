import json
import time
import level
from pprint import pprint
import os
from copy import deepcopy
from utils import printable_grid, generate_random_level_dict

if __name__ == "__main__":
    # with open("resources/level0.json", "r") as level_data_file:
    #     level_data = json.load(level_data_file)
    level_data = generate_random_level_dict(5, "hard")
    env = level.Level(10, 5, level_data, ["Sunflower", "Peashooter"], fps=10)
    actions_taken = []

    while not env.done:
        action = env.sample_action()
        print(f"action: {action}")
        state = env.step(action)
        grid = printable_grid(env)
        pprint(grid)
        print(f"frame num: {env.frame}")
        if action:
            actions_taken.append(action)

    print(f"victory: {env.win}")
    print("actions taken:")
    print(actions_taken)