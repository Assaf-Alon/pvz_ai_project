import json
import time
import level
from pprint import pprint
import os
from copy import deepcopy
from utils import printable_grid, generate_random_level_dict

def play_random():
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


def play_level(level_data, action_list, allowed_plants=["Sunflower", "Peashooter"]):
    env = level.Level(10, 5, level_data, allowed_plants, fps=10)

    while not env.done:
        action = []
        if action_list and env.action_is_legal(action_list[0]):
            action = action_list[0]
            action_list = action_list[1:]
        env.step(action)
        grid = printable_grid(env)
        print(f"Frame: {env.frame}")
        pprint(grid)
        # input()
        # time.sleep(0.03)

if __name__ == "__main__":
    play_random()
    
    # level_data = json.loads("""{
    #     "1": [["Normal", 3]]
    #     }
    # """)
    
    # action_list = [
    #     ["plant", "PotatoMine", 3, 0]
    # ]
    
    # play_level(level_data, action_list, allowed_plants=["PotatoMine"])