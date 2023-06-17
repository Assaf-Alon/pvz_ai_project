import cpp_mcts.mcts as mcts
import cpp_env.level as level
import utils

env = level.Level(5, 10, 10, utils.lvl4_data, utils.chosen_plants_lvl4)
while not env.done:
    print(f"win rate before mcts action: {100 * (env.rollout(8, 10000, 1) / 10000)}%")
    print(f"frame before mcts: {env.frame}")
    action = mcts.run(env, 10, 30, True)

    print(f"frame after mcts: {env.frame}")
    print(utils.action_to_string(action, env))
    while (not env.is_action_legal(action)) and (not env.done): 
        env.step()
    if env.done:
        break
    print(f"frame waiting for step: {env.frame}")
    env.step(action)
    print(f"win rate after mcts action: {100 * (env.rollout(8, 10000, 1) / 10000)}%")
print(f"Game finished with status: {env.win}, at frame number {env.frame}")
# action = mcts.run(env, 3, 300, True)