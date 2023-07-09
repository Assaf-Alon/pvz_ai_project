# import build.mcts
# import build.level
# import build.utils
from build import mcts
from build import level
import utils
from pprint import pprint

env = level.Level(5, 10, 10, *utils.get_level_info("9"), False)
# mcts.run(env, 300, 1, False, 1.4, 0)
# print("====================================", flush=True)
# print("running in mode 0, ucb = 1.4")
# mcts.run(env, 3000, 1, True, 1.4, 0)
# print("====================================", flush=True)
# print("running in mode 0, ucb = 0.1")
# mcts.run(env, 3000, 1, True, 0.1, 0)
# print("====================================", flush=True)
# print("running in mode 0, ucb = 10")
# mcts.run(env, 3000, 1, True, 10, 0)
# print("====================================", flush=True)
# print("running in mode Max, 1 thread")
# mcts.run(env, 3000, 1, True, 1.4, 1)
# print("====================================", flush=True)
# print("running in mode Max, 4 threads")
# mcts.run(env, 3000, 4, True, 1.4, 1)
# print("====================================", flush=True)
# print("running in mode Max, 8 threads")
# mcts.run(env, 3000, 8, True, 1.4, 1)
# print("====================================", flush=True)
# print("running in mode Avg, 1 thread")
# mcts.run(env, 3000, 1, True, 1.4, 2)
# print("====================================", flush=True)
# print("running in mode Avg, 4 threads")
# mcts.run(env, 3000, 4, True, 1.4, 2)
# print("====================================", flush=True)
# print("running in mode Avg, 8 threads")
# mcts.run(env, 3000, 8, True, 1.4, 2)
# print("====================================", flush=True)
# print("running in mode Parallel tree, 1 thread")
# mcts.run(env, 3000, 1, True, 1.4, 3)
# print("====================================", flush=True)
# print("running in mode Parallel tree, 8 threads")
# mcts.run(env, 3000, 8, True, 1.4, 3)
# print("====================================", flush=True)
# print("running in mode Heuristic, 1 thread")
# mcts.run(env, 3000, 1, True, 1.4, 4)
# exit()
base_env = env.clone(-1) # base_env has same level as env
action_list = []
while not env.done:
    print(f"frame before mcts: {env.frame}")
    action = mcts.run(level=env, timeout_ms=200, simulations_per_leaf=8, debug=True, ucb_const=1.4, mode=mcts.AVG_NODE, heuristic_mode=mcts.HEURISTIC_MCTS)
    action_list.append(action)
    print(utils.action_to_string(action))
    env.deferred_step(action)
    print(f"frame after step: {env.frame}")
    print(f"attempting early break", flush=True)
    empty_step_test_level = env.clone(-1) # type: level.Level
    while not empty_step_test_level.done:
        empty_step_test_level.step()
    if empty_step_test_level.win:
        print("early break successful")
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
