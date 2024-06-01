from __future__ import annotations
from pprint import pprint
import time
import pandas as pd

from build import level
from build import mcts
import utils

timestamped_csv = f"test_data/mcts_experiment_{time.time()}.csv"

def try_early_finish(env: level.Level) -> bool:
    """
    Try to finish the game early by doing empty steps, return true if successful
    """
    empty_step_test_level = env.clone(level.FORCE_DETERMINISTIC) # type: level.Level
    while not empty_step_test_level.done:
        empty_step_test_level.step()
    if empty_step_test_level.win:
        while not env.done:
            env.step()
        return True
    return False

def perform_experiment(num_level, time_ms, parallel_factor, ucb_const, rollout_mode, heuristic_mode, selection_mode, loss_heuristic):
    """
    Do an MCTS run using provided parameters, put result in CSV.
    Note: level is an int, indicating the current level num (corresponding to level in game)
    """
    level_data, plant_list = utils.get_level_info(num_level)
    env = level.Level(5, 10, 10, level_data, plant_list, False)
    action_list = []
    start = time.perf_counter()
    while not env.done:
        action = mcts.run(env, int(time_ms), int(parallel_factor), False, float(ucb_const), int(rollout_mode), int(heuristic_mode), int(selection_mode), int(loss_heuristic))
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
        "selection_mode": selection_mode,
        "loss_heuristic": loss_heuristic,
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

def validate_experiment_params(param_list):
    if len(param_list) != 8:
        print("Invalid number of parameters")
        return False
    if param_list[0] not in ["9", "9+", "9++"]:
        print("Invalid level")
        return False
    if param_list[1] not in [100, 200, 300, 400, 500, 600, 700, 800, 1600]:
        print("Invalid time_ms")
        return False
    if param_list[2] not in [2, 4, 6, 8]:
        print("Invalid threads")
        return False
    if param_list[4] not in [mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.PARALLEL_TREES]:
        print("Invalid rollout_mode")
        return False
    if param_list[5] not in [mcts.NO_HEURISTIC, mcts.HEURISTIC_SELECT]:
        print("Invalid heuristic_mode")
        return False
    if param_list[6] not in [mcts.FULL_EXPAND, mcts.SQUARE_RATIO]:
        print("Invalid selection_mode")
        return False
    if param_list[7] not in [mcts.NO_HEURISTIC, mcts.TOTAL_PLANT_COST_HEURISTIC]:
        print("Invalid loss_heuristic")
        return False
    return True

def run_experiments_from_csv(csv_path):
    data = pd.read_csv(csv_path)
    experiment_parameter_list = []
    for _, row in data.iterrows():
        params = [str(row["level"]), int(row["time_ms"]), int(row["threads"]), row["ucb_const"], int(row["rollout_mode"]), int(row["heuristic_mode"]), int(row["selection_mode"]), int(row["loss_heuristic"])]
        experiment_parameter_list.append(params)
    
    pprint(experiment_parameter_list)
    print(f"Parameter space size: {len(experiment_parameter_list)}", flush=True)
    print(f"experiment params valid: {all([validate_experiment_params(x) for x in experiment_parameter_list])}")
    while True: # repeat until stopped manually
        for experiment_parameters in experiment_parameter_list:
            # args = [*experiment_parameters]
            print(f"starting experiment with args: {experiment_parameters}")
            perform_experiment(*experiment_parameters)
            print("----------------------------")

if __name__ == "__main__":
    """
    allowed values in the csv:
    ucb: [0.01, 0.1, 0.2, 0.5, 1.0, 1.4, 2.0, 3.0, 4.0, 5.0, 10, 30, 100, 1000]
    time_ms: >150, 50ms multiples (150,200,250,etc...)
    sim_per_leaf: [2,4,8,12,16,20,30]
    """
    """
    First experiment - general parameters, no heuristics, wide ucb and time ranges
    Values:
    time_range = [100, 200, 300, 400, 500, 600, 700, 800, 1600]
    ucb_range = [0.001, 0.004, 0.016, 0.064, 0.256, 1.024]
    level_range = ["9", "9+", "9++"]
    expansion_modes = [mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.PARALLEL_TREES]
    heuristic_modes = [mcts.NO_HEURISTIC]
    selection_modes = [mcts.FULL_EXPAND]
    loss_heuristic = [mcts.NO_HEURISTIC]
    """
    """
    Second expeirment - heuristics, narrow ucb and time ranges
    Values:
    time_range = [100, 200, 300, 400, 800]
    ucb_range = [0.001, 0.004, 0.016]
    level_range = ["9", "9+", "9++"]
    expansion_modes = [mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.PARALLEL_TREES]
    heuristic_modes = [mcts.NO_HEURISTIC, mcts.HEURISTIC_SELECT]
    selection_modes = [mcts.FULL_EXPAND, mcts.SQUARE_RATIO]
    loss_heuristic = [mcts.NO_HEURISTIC, mcts.TOTAL_PLANT_COST_HEURISTIC]
    """
    run_experiments_from_csv("data/experiment_params.csv")
