from build import mcts
from build import level
import utils
from pprint import pprint

env = level.Level(5, 10, 10, *utils.get_level_info("9+"), False)
base_env = env.clone(-1) # base_env has same level as env
action_list = []
while not env.done:
    print(f"frame before mcts: {env.frame}")
    action = mcts.run(level=env, timeout_ms=1600, simulations_per_leaf=8, debug=True, ucb_const=0.04, mode=mcts.PARALLEL_TREES, heuristic_mode=mcts.HEURISTIC_SELECT, selection_type=mcts.SQUARE_RATIO)
    action_list.append(action)
    print(utils.action_to_string(action))
    env.deferred_step(action)
    print(f"frame after step: {env.frame}")
    print("----------------------------")
print(f"Game finished with status: {env.win}, at frame number {env.frame}")

action_string_list = [utils.action_to_string(action) for action in action_list]
pprint(action_string_list)
print(f"actions taken: {len(action_string_list)}")
input()
utils.simulate_set_game(base_env, action_list)
