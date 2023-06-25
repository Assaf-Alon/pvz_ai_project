import mcts
import level
import utils
from pprint import pprint
import time


# def run(env: level.Level, time_limit_ms):
#     root = mcts.ParralelAvgNode(None, env, level.Action())
#     start = time.perf_counter()
#     end = start + time_limit_ms / 1000
#     while time.perf_counter() < end:

env = level.Level(5, 10, 10, utils.lvl9_data, utils.lvl9_legal_plants)
# start = time.perf_counter()
# mcts.run(env, 3000, 8, True, 1.4, 2)
# print(f"time taken {time.perf_counter() - start}")
# exit()
base_env = env.clone()
action_list = []
while not env.done:
    print(f"frame before mcts: {env.frame}")
    # action = mcts.run(env, 500, 1, True, 1.4)
    # action = mcts.micro_run(env, 500, True)
    action = mcts.run(env, 1500, 8, True, 3, 2)
    action_list.append(action)
    print(f"frame after mcts: {env.frame}")
    print(utils.action_to_string(action))
    env.deferred_step(action)
    print(f"frame after step: {env.frame}")
    # win_rate = 100 * (env.rollout(-1, 10000, 1) / 10000)
    # print(f"win rate after mcts action: {win_rate}%")
    # if win_rate >= 99: # finish loop early if win is already guranteed
    print(f"attempting early break", flush=True)
    empty_step_test_level = env.clone() # type: level.Level
    while not empty_step_test_level.done:
        empty_step_test_level.step()
    if empty_step_test_level.win:
        while not env.done:
            env.step()
        break
    print("----------------------------")
print(f"Game finished with status: {env.win}, at frame number {env.frame}")

action_string_list = [utils.action_to_string(action) for action in action_list]
pprint(action_string_list)
print(f"actions taken: {len(action_string_list)}")
input()
utils.simulate_set_game(base_env, action_list)
