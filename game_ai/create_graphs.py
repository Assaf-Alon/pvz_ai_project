import pandas as pd
from build import mcts
from plot_utils import CSV_FILENAME, filter_and_plot_pvz_data, filter_pvz_data, plot_pvz_data

all_data = pd.read_csv(CSV_FILENAME)
basic_data = filter_pvz_data(
    all_data,
    level=None,
    time_ms_filter={"max": 1600},
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
)


# 5.5.1
data_5_5_1 = filter_pvz_data(
    basic_data,
    level=["1", "2", "4", "6", "7", "9"],
    ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
)

plot_pvz_data(
    data_5_5_1,
    title="Wins vs. Time for different Levels",
    file_name="5.5.1_easy_levels",
    group_graphs_by="level",
    legend_location="lower right",
    legend_size="large",
)


# 5.5.2.1
data_5_5_2_1 = filter_pvz_data(basic_data, level=["9"], ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024])

plot_pvz_data(
    data_5_5_2_1,
    title="Wins vs. Time for different UCBs on Level 9",
    file_name="5.5.2.1_level_9_different_ucb",
    group_graphs_by="ucb_const",
    legend_location="lower right",
    ylim=(0, 1.02),
)


# 5.5.2.2
data_5_5_2_2 = filter_pvz_data(basic_data, level=["9+"], ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024])

plot_pvz_data(
    data_5_5_2_2,
    title="Wins vs. Time for different UCBs on Level 9+",
    file_name="5.5.2.2_level_9+_different_ucb",
    group_graphs_by="ucb_const",
    ylim=(0, 0.5),
    legend_size="large",
)


# 5.5.2.3 + 5.5.2.4 data
data_5_5_2_4 = filter_pvz_data(
    all_data,
    level=["9+"],
    # time_ms_filter={"max": 1600},
    ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.PARALLEL_TREES],
)
data_5_5_2_3 = filter_pvz_data(data_5_5_2_4, time_ms_filter={"max": 1600})
data_5_5_2_4 = filter_pvz_data(data_5_5_2_4, time_ms_filter={"min": 1600})

# 5.5.2.3
plot_pvz_data(
    data_5_5_2_3,
    x_axis="ucb_const",
    title="Wins vs. UCB for different times on Level 9+",
    file_name="5.5.2.3_level_9+_different_ucb_parallel_trees",
    group_graphs_by="time_ms",
    log_scale=True,
    legend_location="upper right",
)


# 5.5.2.4
plot_pvz_data(
    data_5_5_2_4,
    title="Wins vs. Time for different UCBs on Level 9+",
    file_name="5.5.2.4_level_9+_different_ucb_parallel_trees_long_times",
    group_graphs_by="ucb_const",
    legend_location="lower right",
)


data_6_1_1 = filter_pvz_data(
    all_data,
    level=["9", "9+", "9++"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.004],
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE],
)

# 6.1.1.1
data_6_1_1_1 = filter_pvz_data(data_6_1_1, level=["9"], threads_filter=[8])

plot_pvz_data(
    data_6_1_1_1,
    title="Normal Agent vs. Parallel-Max on Level 9",
    file_name="6.1.1.1_level_9_normal_vs_parallel_max",
    group_graphs_by="rollout_mode",
    legend_location="lower right",
    ylim=(0, 1.02),
)


# 6.1.1.2
data_6_1_1_2 = filter_pvz_data(data_6_1_1, level=["9+"], threads_filter=[8])

plot_pvz_data(
    data_6_1_1_2,
    title="Normal Agent vs. Parallel-Max on Level 9+",
    file_name="6.1.1.2_level_9+_normal_vs_parallel_max",
    group_graphs_by="rollout_mode",
    legend_location="upper left",
)


# 6.1.1.2 ++
data_6_1_1_2 = filter_pvz_data(data_6_1_1, level=["9+"], threads_filter=None, expansion_modes_filter=[mcts.MAX_NODE])

plot_pvz_data(
    data_6_1_1_2,
    title="Varying Threads Parallel-Max on Level 9+",
    file_name="6.1.1.2_level_9+_parallel_max_threads",
    group_graphs_by="threads",
    legend_location="lower right",
)


# 6.1.1.3
data_6_1_1_3 = filter_pvz_data(data_6_1_1, level=["9++"], threads_filter=[8])

plot_pvz_data(
    data_6_1_1_3,
    title="Normal Agent vs. Parallel-Max on Level 9++",
    file_name="6.1.1.3_level_9++_normal_vs_parallel_max",
    group_graphs_by="rollout_mode",
    legend_location="upper left",
)

# 6.1.2.1
data_6_1_2 = filter_pvz_data(
    all_data,
    level=["9", "9+", "9++"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.004],
    threads_filter=[8],
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.PARALLEL_TREES],
)

data_6_1_2_1 = filter_pvz_data(data_6_1_2, level=["9"])

plot_pvz_data(
    data_6_1_2_1,
    title="Normal Agent vs. Parallel-Max vs. Parallel-Trees on Level 9",
    file_name="6.1.2.1_level_9_parallelizations",
    group_graphs_by="rollout_mode",
    legend_location="lower right",
    ylim=(0, 1.02),
)

# 6.1.2.2
data_6_1_2_2 = filter_pvz_data(data_6_1_2, level=["9+"])

plot_pvz_data(
    data_6_1_2_2,
    title="Normal Agent vs. Parallel-Max vs. Parallel-Trees on Level 9+",
    file_name="6.1.2.2_level_9+_parallelizations",
    group_graphs_by="rollout_mode",
    legend_location="center right",
)


# 6.1.2.3
data_6_1_2_3 = filter_pvz_data(data_6_1_2, level=["9++"])

plot_pvz_data(
    data_6_1_2_3,
    title="Normal Agent vs. Parallel-Max vs. Parallel-Trees on Level 9++",
    file_name="6.1.2.3_level_9++_parallelizations",
    group_graphs_by="rollout_mode",
    legend_location="upper left",
)


# 6.1.3
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Parallel Trees With Alternative Selection Policy on Level 9++",
    file_name="6.1.3_level_9++_selection",
    level=["9++"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND, mcts.SQUARE_RATIO],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.PARALLEL_TREES],
    group_graphs_by="selection_mode",
    legend_location="upper left",
)


# 6.2.1
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Algent With Selection Heuristic (Tie-Breaker) on Level 9+",
    file_name="6.2.1_level_9+_selection_heuristic",
    level=["9+"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC, mcts.HEURISTIC_SELECT],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    group_graphs_by="heuristic_mode",
    legend_location="upper left",
)


# 6.2.2.2
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Algent With Loss Heuristic on Level 9+",
    file_name="6.2.2.2_level_9+_loss_heuristic",
    level=["9+"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC, mcts.TOTAL_PLANT_COST_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    group_graphs_by="loss_heuristic",
    legend_location="upper left",
    ylim=(0, 0.5),
)


# 6.2.2.2 +
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Algent With Loss Heuristic on Level 9+",
    file_name="6.2.2.2_level_9+_loss_heuristic2",
    level=["9+"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=None,
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    group_graphs_by="loss_heuristic",
    legend_location="upper left",
    ylim=(0, 0.5),
)


# 6.3.1
data_6_3_1 = filter_pvz_data(
    all_data,
    level=["9+"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.004],
    heuristic_modes_filter=[mcts.NO_HEURISTIC, mcts.HEURISTIC_SELECT],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC, mcts.TOTAL_PLANT_COST_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
)

data_6_3_1_0 = filter_pvz_data(
    data_6_3_1.copy(),
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
)
data_6_3_1_0["name_in_legend"] = "No Heuristics"

data_6_3_1_1 = filter_pvz_data(
    data_6_3_1.copy(),
    heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
)
data_6_3_1_1["name_in_legend"] = "Selection Heuristic"

data_6_3_1_2 = filter_pvz_data(
    data_6_3_1.copy(),
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
)
data_6_3_1_2["name_in_legend"] = "Plant Cost Loss Heuristic"

data_6_3_1_3 = filter_pvz_data(
    data_6_3_1.copy(),
    heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
    loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
)
data_6_3_1_3["name_in_legend"] = "Both Heuristics"

data_6_3_1 = pd.concat([data_6_3_1_0, data_6_3_1_1, data_6_3_1_2, data_6_3_1_3], ignore_index=True)

plot_pvz_data(
    data_6_3_1,
    x_axis="time_ms",
    title="Combination of Heuristics on Level 9+",
    file_name="6.3.1_heuristics_combinations",
    group_graphs_by="name_in_legend",
    legend_location="upper left",
    sort_legend=False,
)
