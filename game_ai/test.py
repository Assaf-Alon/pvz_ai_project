# import cpp_mcts.mcts as mcts
# import cpp_env.level as level
import mcts
import level
import utils

env = level.Level(5, 10, 10, utils.lvl4_data, utils.chosen_plants_lvl4)
base_env = env.clone()
action_list = []
while not env.done:
    print(f"win rate before mcts action: {100 * (env.rollout(8, 10000, 1) / 10000)}%")
    print(f"frame before mcts: {env.frame}")
    action, rollouts = mcts.run(env, 30000, 1, True)
    action_list.append(action)
    print(f"frame after mcts: {env.frame}")
    print(utils.action_to_string(action))
    while (not env.is_action_legal(action)) and (not env.done): 
        env.step()
    if env.done:
        break
    print(f"frame waiting for step: {env.frame}")
    env.step(action)
    print(f"win rate after mcts action: {100 * (env.rollout(8, 10000, 1) / 10000)}%")
print(f"Game finished with status: {env.win}, at frame number {env.frame}")

utils.simulate_set_game(base_env, action_list)

# num_rollouts = 10000
# winrate = 100 * (env.rollout(8, num_rollouts, 1) / num_rollouts)
# print(f"winrate before: {winrate}%")

# def get_winrate_percent(env, action: level.Action):
#     env_clone = env.clone() # type: level.Level
#     while not env_clone.is_action_legal(action): 
#         env_clone.step()
#     env_clone.step(action)
#     wins = env.rollout(8, num_rollouts, 1)
#     return 100 * (wins / num_rollouts)

# def play_5_mcts_steps(env, secs, rollouts):
#     env_clone = env.clone() # type: level.Level
#     for _ in range(5):
#         print(f"current frame: {env_clone.frame}", flush=True)
#         action, rollouts = mcts.run(env_clone, secs, rollouts)
#         print(f"Action chosen: {action}", flush=True)
#         while not env_clone.is_action_legal(action) and not env_clone.done:
#             env_clone.step()
#         if env_clone.done:
#             print("what the hell", flush=True)
#         env_clone.step(action)
#     print(f"for {rollouts} rollouts per leaf, got {get_winrate_percent(env_clone,action)}% winrate", flush=True)
    

# def dumb_optimize(env: level.Level, secs: int):
#     print(f"optimizing num rollouts for {secs}s MCTS", flush=True)
#     for i in range(1, 50, 2):
#         # action, rollouts = mcts.run(env, secs, i)
#         play_5_mcts_steps(env, secs, i)
#         # print(f"for {i} rollouts per leaf, got {rollouts} with {get_winrate_percent(action)}% winrate")

# dumb_optimize(env, 1)

# # for lane in range(5):
# #     for col in range(10):
# #         action = level.Action(14, lane, col)
# #         env_clone = env.clone() # type: level.Level
# #         winrate = 100 * (env.rollout(8, 50000, 1) / 50000) 
# #         print(f"lane: {lane}, col: {col}, winrate: {winrate}")

