from mcts import mcts

NORMAL_MCTS = mcts.NORMAL_MCTS
MAX_NODE = mcts.MAX_NODE
AVG_NODE = mcts.AVG_NODE
PARALLEL_TREES = mcts.PARALLEL_TREES

NO_HEURISTIC = mcts.NO_HEURISTIC
# HEURISTIC_MCTS = mcts.HEURISTIC_MCTS
HEURISTIC_SELECT = mcts.HEURISTIC_SELECT
# HEURISTIC_EXPAND = mcts.HEURISTIC_EXPAND

selection_modes = [mcts.FULL_EXPAND, mcts.SQUARE_RATIO]
selection_mode_to_name = {
    mcts.FULL_EXPAND: "full expand",
    mcts.SQUARE_RATIO: "square ratio"
}
loss_heuristic = [mcts.NO_HEURISTIC, mcts.TOTAL_PLANT_COST_HEURISTIC]
loss_heuristic_to_name = {
    mcts.NO_HEURISTIC: "no heuristic",
    mcts.TOTAL_PLANT_COST_HEURISTIC: "total plant cost",
    mcts.TOTAL_ZOMBIE_HP_HEURISTIC: "total zombie hp",
    mcts.ZOMBIES_LEFT_TO_SPAWN_HEURISTIC: "zombies left to spawn",
    mcts.FRAME_HEURISTIC: "frame"
}
rollout_mode_to_name = {
    NORMAL_MCTS: "normal",
    MAX_NODE: "parallel max",
    AVG_NODE: "parallel avg",
    PARALLEL_TREES: "parallel trees",
}
heuristic_mode_to_name = {
    NO_HEURISTIC: "no heuristic",
    # HEURISTIC_MCTS: "full heuristic",
    # HEURISTIC_EXPAND: "expand heuristic",
    HEURISTIC_SELECT: "select heuristic"
}

selection_mode_name_to_mode = {v: k for k, v in selection_mode_to_name.items()}
loss_heuristic_name_to_mode = {v: k for k, v in loss_heuristic_to_name.items()}
rollout_mode_name_to_mode = {v: k for k, v in rollout_mode_to_name.items()}
heuristic_mode_name_to_mode = {v: k for k, v in heuristic_mode_to_name.items()}