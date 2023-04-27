import sys
sys.path.append("../")
import consts

import os

import unittest
import json
import time
import difflib
import level

from pprint import pprint
from utils import printable_grid

LANES = 5
COLUMNS = 10
FPS = 10
MAX_FRAME = 9999

EXPECTED_FILE = "tests/output/level2.txt"
ACTUAL_FILE = "tests/output/actual2.txt"
LEVEL_JSON  = "tests/levels/level2.json"

if os.path.exists(ACTUAL_FILE):
    os.remove(ACTUAL_FILE)


class TestLevel2(unittest.TestCase):
    def test_level2(self):
        with open(LEVEL_JSON, "r") as level_data_file:
            level_data = json.load(level_data_file)
        env = level.Level(COLUMNS, LANES, level_data, False, fps=FPS, logfile=ACTUAL_FILE)
        action_list = [
            ["plant", "sunflower", 0, 0],
            ["plant", "sunflower", 1, 0],
            ["plant", "peashooter", 1, 1],
            ["plant", "peashooter", 2, 1]
        ]
        
        while not env.done and env.frame <= MAX_FRAME:
            action = []
            if action_list and env.action_is_legal(action_list[0]):
                action = action_list[0]
                action_list = action_list[1:]
            env.step(action)
            grid = printable_grid(env)
            pprint(grid)
            
        with open(EXPECTED_FILE) as file:
            expected = file.readlines()
        
        with open(ACTUAL_FILE) as file:
            actual = file.readlines()
        
        difflib.context_diff(expected, actual)
        
        print(f"Diff: ")
        passed = True
        for line in difflib.unified_diff(
            expected, actual, fromfile=EXPECTED_FILE,
            tofile=ACTUAL_FILE, lineterm=''):
            passed = False
            print(line)
        self.assertTrue(passed)

    
# if __name__ == "__main__":