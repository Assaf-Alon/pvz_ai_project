import pandas as pd
from build import mcts
from plot_utils import (
    CSV_FILENAME,
    filter_and_plot_pvz_data,
    filter_pvz_data,
    plot_pvz_data,
)


def plot_pvz_data_section_6_3(
    all_data: pd.DataFrame,
    level: str,
    rollout_mode: str,
    file_name: str,
    title: str,
    legend_location: str = "upper left",
):
    data_combined = filter_pvz_data(
        all_data,
        level=[level],
        time_ms_filter={"max": 1600},
        ucb_filter=[0.004],
        # heuristic_modes_filter=[mcts.NO_HEURISTIC, mcts.HEURISTIC_SELECT],
        # selection_modes_filter=[mcts.FULL_EXPAND, mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.NO_HEURISTIC, mcts.TOTAL_PLANT_COST_HEURISTIC],
        expansion_modes_filter=[rollout_mode],
    )

    data_0 = filter_pvz_data(
        data_combined.copy(),
        heuristic_modes_filter=[mcts.NO_HEURISTIC],
        selection_modes_filter=[mcts.FULL_EXPAND],
        loss_heuristics_filter=[mcts.NO_HEURISTIC],
    )
    data_0["name_in_legend"] = "No Heuristics"

    data_1 = filter_pvz_data(
        data_combined.copy(),
        heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
        selection_modes_filter=[mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.NO_HEURISTIC],
    )
    data_1["name_in_legend"] = "Selection Heuristic + Selection Policy"

    data_2 = filter_pvz_data(
        data_combined.copy(),
        heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
        selection_modes_filter=[mcts.FULL_EXPAND],
        loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
    )
    data_2["name_in_legend"] = "Selection Heuristic + Loss Heuristic"

    data_3 = filter_pvz_data(
        data_combined.copy(),
        heuristic_modes_filter=[mcts.NO_HEURISTIC],
        selection_modes_filter=[mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
    )
    data_3["name_in_legend"] = "Selection Policy + Loss Heuristic"

    data_4 = filter_pvz_data(
        data_combined.copy(),
        heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
        selection_modes_filter=[mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
    )
    data_4["name_in_legend"] = "All Improvements"

    data_combined = pd.concat([data_0, data_1, data_2, data_3, data_4], ignore_index=True)

    plot_pvz_data(
        data_combined,
        title=title,
        file_name=file_name,
        group_graphs_by="name_in_legend",
        legend_location=legend_location,
        sort_legend=False,
    )


def plot_pvz_data_all_improvements(
    all_data: pd.DataFrame,
    level: str,
    file_name: str,
    title: str,
    legend_location: str = "upper left",
):
    data_6_3_4 = filter_pvz_data(
        all_data,
        level=[level],
        time_ms_filter={"max": 1600},
        ucb_filter=[0.004],
        # heuristic_modes_filter=[mcts.NO_HEURISTIC, mcts.HEURISTIC_SELECT],
        # selection_modes_filter=[mcts.FULL_EXPAND, mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.NO_HEURISTIC, mcts.TOTAL_PLANT_COST_HEURISTIC],
        # expansion_modes_filter=[rollout_mode],
    )

    data_6_3_4_0 = filter_pvz_data(
        data_6_3_4.copy(),
        heuristic_modes_filter=[mcts.NO_HEURISTIC],
        selection_modes_filter=[mcts.FULL_EXPAND],
        loss_heuristics_filter=[mcts.NO_HEURISTIC],
        expansion_modes_filter=[mcts.NORMAL_MCTS],
    )
    data_6_3_4_0["name_in_legend"] = "Basic Agent"

    data_6_3_4_1 = filter_pvz_data(
        data_6_3_4.copy(),
        heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
        selection_modes_filter=[mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
        expansion_modes_filter=[mcts.NORMAL_MCTS],
    )
    data_6_3_4_1["name_in_legend"] = "Full Heuristic Agent"

    data_6_3_4_2 = filter_pvz_data(
        data_6_3_4.copy(),
        heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
        selection_modes_filter=[mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
        expansion_modes_filter=[mcts.MAX_NODE],
    )
    data_6_3_4_2["name_in_legend"] = "Parallel Max + Full Heuristic Agent"

    data_6_3_4_3 = filter_pvz_data(
        data_6_3_4.copy(),
        heuristic_modes_filter=[mcts.HEURISTIC_SELECT],
        selection_modes_filter=[mcts.SQUARE_RATIO],
        loss_heuristics_filter=[mcts.TOTAL_PLANT_COST_HEURISTIC],
        expansion_modes_filter=[mcts.PARALLEL_TREES],
    )
    data_6_3_4_3["name_in_legend"] = "Parallel Trees + Full Heuristic Agent"

    data_6_3_4 = pd.concat([data_6_3_4_0, data_6_3_4_1, data_6_3_4_2, data_6_3_4_3], ignore_index=True)

    plot_pvz_data(
        data_6_3_4,
        title=title,
        file_name=file_name,
        group_graphs_by="name_in_legend",
        legend_location=legend_location,
        sort_legend=False,
    )


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
    hue_order=["1", "2", "4", "6", "7", "9"],
)


# 5.5.2.1
data_5_5_2_1 = filter_pvz_data(
    basic_data,
    level=["9"],
    ucb_filter=[0.00001, 0.0001, 0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
)

plot_pvz_data(
    data_5_5_2_1,
    title="Wins vs. Time for different UCBs on Level 9",
    file_name="5.5.2.1_level_9_different_ucb",
    group_graphs_by="ucb_const",
    legend_location="lower right",
    ylim=(0, 1.02),
)


# 5.5.2.2
data_5_5_2_2 = filter_pvz_data(
    basic_data,
    level=["9+"],
    ucb_filter=[0.00001, 0.0001, 0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
)

plot_pvz_data(
    data_5_5_2_2,
    title="Wins vs. Time for different UCBs on Level 9+",
    file_name="5.5.2.2_level_9+_different_ucb",
    group_graphs_by="ucb_const",
    ylim=(0, 0.5),
)

data_5_5_2_2_extra1 = filter_pvz_data(
    all_data.copy(),
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    level=["9"],
    time_ms_filter={"min": 200, "max": 200},
)
data_5_5_2_2_extra1["name_in_legend"] = "Basic Agent on Level 9 with 200ms Limit"

data_5_5_2_2_extra2 = filter_pvz_data(
    all_data.copy(),
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.PARALLEL_TREES],
    level=["9+"],
    time_ms_filter={"min": 300, "max": 300},
)
data_5_5_2_2_extra2["name_in_legend"] = "Parallel Trees Agent on Level 9++ with 300ms Limit"

data_5_5_2_2_extra3 = filter_pvz_data(
    all_data.copy(),
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    level=["9+"],
    time_ms_filter={"min": 1600, "max": 1600},
)
data_5_5_2_2_extra3["name_in_legend"] = "Basic Agent on Level 9+ with 1600ms Limit"

data_5_5_2_2_extra = pd.concat([data_5_5_2_2_extra1, data_5_5_2_2_extra2, data_5_5_2_2_extra3], ignore_index=True)
ucbs_x = [0.001, 0.004, 0.016, 0.032]
ucbs_xi = list(range(len(ucbs_x)))

plot_pvz_data(
    data_5_5_2_2_extra,
    title="UCB Comparison For Different Parameters",
    file_name="5.5.2.2_different_ucbs_general_params",
    group_graphs_by="name_in_legend",
    legend_location="upper left",
    legend_size="small",
    sort_legend=False,
    x_axis="ucb_const",
    ylim=(0, 1.5),
    log_scale=True,
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
data_6_1_1_2 = filter_pvz_data(
    data_6_1_1,
    level=["9+"],
    threads_filter=None,
    expansion_modes_filter=[mcts.MAX_NODE],
)

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
plot_pvz_data_section_6_3(
    all_data,
    "9+",
    mcts.NORMAL_MCTS,
    "6.3.1_heuristics_combinations",
    "Combination of Heuristics on Level 9+",
)

# 6.3.2
plot_pvz_data_section_6_3(
    all_data,
    "9+",
    mcts.MAX_NODE,
    "6.3.2.1_heuristics_combinations",
    "Parallel MAX and Heuristics on Level 9+",
    "lower right",
)

plot_pvz_data_section_6_3(
    all_data,
    "9++",
    mcts.MAX_NODE,
    "6.3.2.2_heuristics_combinations",
    "Parallel MAX and Heuristics on Level 9++",
)

# 6.3.3
plot_pvz_data_section_6_3(
    all_data,
    "9++",
    mcts.PARALLEL_TREES,
    "6.3.3_heuristics_combinations",
    "Parallel Trees and Heuristics on Level 9++",
    "lower right",
)


# 6.3.4
plot_pvz_data_all_improvements(all_data, "9+", "6.3.4.1_all_improvements", "Comparing All Improvements on Level 9+")
plot_pvz_data_all_improvements(
    all_data,
    "9++",
    "6.3.4.2_all_improvements",
    "Comparing All Improvements on Level 9++",
)
