import mcts
import level
import utils
from pprint import pprint

env = level.Level(5, 10, 10, utils.lvl9_data, utils.lvl9_legal_plants)
base_env = env.clone()
action_list = []
while not env.done:
    print(f"frame before mcts: {env.frame}")
    action = mcts.run(env, 500, 1, True, 1.4)
    action_list.append(action)
    print(f"frame after mcts: {env.frame}")
    print(utils.action_to_string(action))
    env.deferred_step(action)
    print(f"frame after step: {env.frame}")
    win_rate = 100 * (env.rollout(-1, 10000, 1) / 10000)
    print(f"win rate after mcts action: {win_rate}%")
    if win_rate >= 99: # finish loop early if win is already guranteed
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
print(f"actions tanke: {len(action_string_list)}")
input()
utils.simulate_set_game(base_env, action_list)
