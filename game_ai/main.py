from build import mcts, level
import utils

level_data, plant_list = utils.get_level_info("9")
env = level.Level(5, 10, 10, level_data, plant_list, False)
actions = []
observations = []
while not env.done:
    action = mcts.run(
        level=env,
        timeout_ms=400,
        simulations_per_leaf=8,
        debug=True,
        ucb_const=0.04,
        mode=mcts.PARALLEL_TREES,
        heuristic_mode=mcts.HEURISTIC_SELECT,
        selection_type=mcts.SQUARE_RATIO,
        loss_heuristic=mcts.TOTAL_PLANT_COST_HEURISTIC
    )
    actions.append(action)
    while not env.is_action_legal(action):
        env.step()
        utils.draw_observation(env.get_observation(), env.frame)
    env.step(action)
    utils.draw_observation(env.get_observation(), env.frame)
    print("-------------------------------------")
    print(f"[{env.frame}] Action chosen: lane: {action.lane}, col: {action.col}, plant: {utils.plant_to_name[action.plant_name]}")
    print(f"lawnmowers: {env.lawnmowers[0]} {env.lawnmowers[1]} {env.lawnmowers[2]} {env.lawnmowers[3]} {env.lawnmowers[4]}")

print(f"Game finished with status: {env.win}, at frame number {env.frame}")
