from __future__ import annotations
from pprint import pprint
import itertools
import sys
import time
import random

from build import level
from build import mcts
import utils

timestamped_csv = f"test_data/mcts_experiment_{random.randint(1, 999)}.csv"

def try_early_finish(env: level.Level) -> bool:
    """
    Try to finish the game early by doing empty steps, return true if successful
    """
    empty_step_test_level = env.clone(-1) # type: level.Level
    while not empty_step_test_level.done:
        empty_step_test_level.step()
    if empty_step_test_level.win:
        while not env.done:
            env.step()
        return True
    return False

def perform_experiment(num_level, time_ms, parallel_factor, ucb_const, rollout_mode, heuristic_mode):
    """
    Do an MCTS run using provided parameters, put result in CSV.
    Note: level is an int, indicating the current level num (corresponding to level in game)
    """
    level_data, plant_list = utils.get_level_info(num_level)
    env = level.Level(5, 10, 10, level_data, plant_list, False)
    action_list = []
    start = time.perf_counter()
    while not env.done:
        action = mcts.run(env, int(time_ms), int(parallel_factor), False, float(ucb_const), int(rollout_mode), int(heuristic_mode))
        env.deferred_step(action)
        action_list.append(action)
        # # To view the choices in each step
        # print("-------------------------------------")
        # print(f"[{env.frame}] Action chosen: lane: {action.lane}, col: {action.col}, plant: {utils.plant_to_name[action.plant_name]}")
        # print(f"lawnmowers: {env.lawnmowers[0]} {env.lawnmowers[1]} {env.lawnmowers[2]} {env.lawnmowers[3]} {env.lawnmowers[4]}")
        # input("Press enter")
        try_early_finish(env)
    end = time.perf_counter()
    result_dict = {
        "level": num_level,
        "time_ms": time_ms,
        "parallel_factor": parallel_factor,
        "ucb_const": ucb_const,
        "rollout_mode": rollout_mode,
        "heuristic_mode": heuristic_mode,
        "win": env.win,
        "num_steps": len(action_list)
    }
    expected_time = (time_ms * len(action_list)) / 1000
    actual_time = end - start
    pprint(result_dict)
    if (actual_time > expected_time * 1.1):
        print('\033[91m' + f"WARNING: experiment took {actual_time} seconds, expected time: {expected_time}, difference {100 * (actual_time - expected_time) / expected_time:.2f}%" + '\033[0m')
    else:
        print(f"experiment took {end - start} seconds, expected time: {expected_time}", flush=True)
    utils.csv_append(result_dict, timestamped_csv)


if __name__ == "__main__":
    """
    allowed values in the csv:
    ucb: [0.01, 0.1, 0.2, 0.5, 1.0, 1.4, 2.0, 3.0, 4.0, 5.0, 10, 30, 100, 1000]
    time_ms: >150, 50ms multiples (150,200,250,etc...)
    sim_per_leaf: [2,4,8,12,16,20,30]
    """
    # time_range = range(150, 800, 50)
    # time_range = range(200, 1100, 100)
    time_range = [200, 400, 800]
    ucb_range = [0.2, 1.4, 30]
    level_range = ["9", "9+"]
    heuristic_modes = [mcts.NO_HEURISTIC, mcts.HEURISTIC_MCTS, mcts.HEURISTIC_EXPAND, mcts.HEURISTIC_SELECT]
    # ucb_range = [0, 0.1, 0.2, 0.5, 1.0, 1.4, 3.0, 10, 30, 100]
    # ucb_range = [0.2, 1.4]
    # ucb_range = [3, 30]
    # ucb_range = [20, 40] # zeroing in on optimal mode2 ucb
    # ucb_range = [25, 35] # zeroing in on optimal mode2 ucb

    # sim_per_leaf_range = [2,4,8,12,16,20,30]
    # rollot_mode_range = [0,1,2]
    parallel_parameter_list = list(itertools.product(level_range, time_range, [8], ucb_range, [mcts.MAX_NODE,mcts.AVG_NODE,mcts.PARALLEL_TREES], heuristic_modes))
    traditional_parameter_list = list(itertools.product(level_range, time_range, [1], ucb_range, [mcts.NORMAL_MCTS], heuristic_modes))
    experiment_parameter_list = parallel_parameter_list + traditional_parameter_list
    # experiment_parameter_list = list(itertools.product(["9"], time_range, [8], ucb_range, [mcts.AVG_NODE]))
    ## Full experiment parameter list
    # experiment_parameter_list = list(itertools.product(time_range, sim_per_leaf_range, ucb_range, rollot_mode_range))
    ## Parallel experiment only, optimize for thread num
    # experiment_parameter_list = list(itertools.product(time_range, sim_per_leaf_range, ucb_range, [1,2]))
    print(f"Parameter space size: {len(experiment_parameter_list)}")
    while True: ## run experiments until stopped manually
        for experiment_parameters in experiment_parameter_list:
            # args = [*experiment_parameters]
            print(f"starting experiment with args: {experiment_parameters}")
            perform_experiment(*experiment_parameters)
            print("----------------------------")
