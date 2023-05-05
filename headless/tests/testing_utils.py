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
MAX_FRAME = 1200

PRINT_OUTPUT = False
TEST_SLOW = False

def get_file_names(number, plant=""):
    file_id = f"{plant}_{number}" if plant else f"level_{number}"
    return (f"tests/expected/{file_id}.txt",
           f"tests/output/{file_id}.txt",
           f"tests/levels/{file_id}.json")

def setup_test(num, plant=""):
    EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = get_file_names(num, plant)
    if os.path.exists(ACTUAL_FILE):
        os.remove(ACTUAL_FILE)

    with open(LEVEL_JSON, "r") as level_data_file:
        level_data = json.load(level_data_file)
    env = level.Level(COLUMNS, LANES, level_data, chosen_plants=["Peashooter", "Sunflower"], fps=FPS, logfile=ACTUAL_FILE)
    
    return (env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON)

def play_game(env: level.Level, action_list):
    while not env.done and env.frame <= MAX_FRAME:
        action = []
        if action_list and env.action_is_legal(action_list[0]):
            action = action_list[0]
            action_list = action_list[1:]
        env.step(action)
        if PRINT_OUTPUT:
            grid = printable_grid(env)
            pprint(grid)
            if TEST_SLOW:
                time.sleep(0.03)

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

def update_tests():
    import shutil
    src_dir = "tests/output"
    dst_dir = "tests/expected"
    # files = os.listdir(src_dir)
    # shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
