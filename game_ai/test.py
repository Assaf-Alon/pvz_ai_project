# import build.mcts
# import build.level
# import build.utils
from build import mcts
from build import level
import utils
from pprint import pprint

env = level.Level(5, 10, 10, *utils.get_level_info(9), False)
base_env = env.clone(-1) # base_env has same level as env
action_list = []
while not env.done:
    print(f"frame before mcts: {env.frame}")
    action = mcts.run(level=env, timeout_ms=300, games_per_rollout=8, debug=False, ucb_const=3, rollout_mode=3)
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
