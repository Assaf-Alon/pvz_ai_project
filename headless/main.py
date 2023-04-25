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
    action_list = [
        ["plant", "sunflower", 0, 0],
        ["plant", "sunflower", 1, 0],
        ["plant", "peashooter", 1, 1],
        ["plant", "peashooter", 2, 1]
    ]
    while not env.done:
        action = []
        if action_list and env.action_is_legal(action_list[0]):
            action = action_list[0]
            action_list = action_list[1:]
        print(action)
        env.step(action)
        grid = printable_grid(env)
        pprint(grid)
        print(f"frame num: {env.frame}")
        print(f"suns: {env.suns}")
        for zombie in env.zombies:
            print(f"Zombie: {zombie.pos} , HP={zombie.hp}")
        state = env.construct_state()
        for lane in state[2]:
            for square in lane:
                print(square, end='')
            print()
        # print("---------------")
        # for plant in env.plants:
        #     print(f"Plant: {plant.position} , HP={plant.hp}")
        # for bullet in env.bullets:
        #     print(f"Bullet [{bullet.lane}, {bullet.column}]")
        time.sleep(0.1)
        # input()
        # os.system('clear')
        # os.system('cls')