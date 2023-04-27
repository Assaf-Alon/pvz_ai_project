import sys
sys.path.append("../")
import consts

import os
if os.path.exists(consts.LOG_FILE_NAME):
    os.remove(consts.LOG_FILE_NAME)

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
MAX_FRAME = 700





def get_file_names(number):
    return (f"tests/output/level{number}.txt",
           f"tests/output/actual{number}.txt",
           f"tests/levels/level{number}.json")

def setup_test(num):
    EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = get_file_names(num)
    if os.path.exists(ACTUAL_FILE):
        os.remove(ACTUAL_FILE)

    with open(LEVEL_JSON, "r") as level_data_file:
        level_data = json.load(level_data_file)
    env = level.Level(COLUMNS, LANES, level_data, False, fps=FPS, logfile=ACTUAL_FILE)
    
    return (env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON)

def play_game(env: level.Level, action_list):
    while not env.done and env.frame <= MAX_FRAME:
        action = []
        if action_list and env.action_is_legal(action_list[0]):
            action = action_list[0]
            action_list = action_list[1:]
        env.step(action)
        grid = printable_grid(env)
        pprint(grid)

def compare_results(expected_file, actual_file):
    with open(expected_file) as file:
        expected = file.readlines()
    
    with open(actual_file) as file:
        actual = file.readlines()
    
    difflib.context_diff(expected, actual)
    
    print(f"Diff: ")
    passed = True
    for line in difflib.unified_diff(
        expected, actual, fromfile=expected_file,
        tofile=actual_file, lineterm=''):
        passed = False
        print(line)
    return passed
class TestLevel1(unittest.TestCase):
    def test_level1(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1")
        
        action_list = [
            ["plant", "sunflower", 0, 0],
            ["plant", "sunflower", 1, 0],
            ["plant", "peashooter", 1, 1],
            ["plant", "peashooter", 2, 1]
        ]
        
        play_game(env, action_list)
        
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    
    def test_level2(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2")
        
        action_list = [
            ["plant", "sunflower", 0, 0],
            ["plant", "sunflower", 1, 0],
            ["plant", "peashooter", 1, 1],
            ["plant", "peashooter", 2, 1]
        ]
        
        play_game(env, action_list)
        
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    

    
# if __name__ == "__main__":