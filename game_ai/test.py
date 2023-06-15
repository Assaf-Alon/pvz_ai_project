import cpp_mcts.mcts as mcts
import cpp_env.level as level
import utils

env = level.Level(5, 10, 10, utils.lvl4_data, utils.chosen_plants_lvl4)
while not env.done:
    action = mcts.run(env, 10, 500)
    print(utils.action_to_string(action, env))
    while not env.is_action_legal(action) and not env.done: env.step()
    if env.done:
        break
    env.step(action)
print(f"Game finished with status: {env.win}, at frame number {env.frame}")
