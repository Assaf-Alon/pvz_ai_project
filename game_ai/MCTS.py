from __future__ import annotations
from pprint import pprint
import sys

import level
import mcts
import utils

def try_early_finish(env: level.Level) -> bool:
    """
    Try to finish the game early by doing empty steps, return true if successful
    """
    empty_step_test_level = env.clone() # type: level.Level
    while not empty_step_test_level.done:
        empty_step_test_level.step()
    if empty_step_test_level.win:
        while not env.done:
            env.step()
        return True
    return False

def perform_experiment(num_level, time_ms, threads, ucb_const, rollout_mode):
    """
    Do an MCTS run using provided parameters, put result in CSV.
    Note: level is an int, indicating the current level num (corresponding to level in game)
    """
    level_data, plant_list = utils.get_level_info(num_level)
    env = level.Level(5, 10, 10, level_data, plant_list)
    action_list = []
    while not env.done:
        action = mcts.run(env, int(time_ms), int(threads), False, float(ucb_const), int(rollout_mode))
        env.deferred_step(action)
        action_list.append(action)
        # # To view the choices in each step
        # print("-------------------------------------")
        # print(f"[{env.frame}] Action chosen: lane: {action.lane}, col: {action.col}, plant: {utils.plant_to_name[action.plant_name]}")
        # print(f"lawnmowers: {env.lawnmowers[0]} {env.lawnmowers[1]} {env.lawnmowers[2]} {env.lawnmowers[3]} {env.lawnmowers[4]}")
        # input("Press enter")
        try_early_finish(env)
    result_dict = {
        "level": num_level,
        "time_ms": time_ms,
        "threads": threads,
        "ucb_const": ucb_const,
        "rollout_mode": rollout_mode,
        "win": env.win,
        "num_steps": len(action_list)
    }
    pprint(result_dict)
    utils.csv_append(result_dict)


if __name__ == "__main__":
    # args = [sys.argv[i] for i in range(1, len(sys.argv))]
    for i in range(1, 20):
        args = [9, 100 * i, 8, 1.4, 0]
        for j in range(1, 10):
            print(f"starting experiment with args: {args}")
            perform_experiment(*args)
    # args = ["9+", 5000, 8, 1.4, 0]
    # perform_experiment(*args)
    