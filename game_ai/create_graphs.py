import math
from typing import Dict, List, Tuple, Union
from build import level
from build import mcts
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from pprint import pprint
from time import time
import json
import csv


CSV_FILENAME = "data/all.csv"
plant_to_name = (
    "no_plant",
    "cherrybomb",
    "chomper",
    "hypnoshroom",
    "iceshroom",
    "jalapeno",
    "peashooter",
    "potatomine",
    "puffshroom",
    "repeaterpea",
    "scaredyshroom",
    "snowpea",
    "spikeweed",
    "squash",
    "sunflower",
    "sunshroom",
    "threepeater",
    "wallnut",
)

to_legend = {
    "heuristic_mode": {mcts.NO_HEURISTIC: "No Heuristic", mcts.HEURISTIC_SELECT: "Selection Heuristic"},
    "selection_mode": {mcts.FULL_EXPAND: "Full Expand (Normal)", mcts.SQUARE_RATIO: "Square Ratio"},
    "loss_heuristic": {
        mcts.NO_HEURISTIC: "No Heuristic",
        mcts.FRAME_HEURISTIC: "Frame Heuristic",
        mcts.TOTAL_PLANT_COST_HEURISTIC: "Plant Cost Heuristic",
        mcts.TOTAL_ZOMBIE_HP_HEURISTIC: "Total Zombie HP Heuristic",
        mcts.ZOMBIES_LEFT_TO_SPAWN_HEURISTIC: "Zombies to Spawn Heuristic",
    },
    "rollout_mode": {
        mcts.NORMAL_MCTS: "No Parallelization",
        mcts.MAX_NODE: "Parallel MAX",
        mcts.AVG_NODE: "Parallel AVG",
        mcts.PARALLEL_TREES: "Parallel TREES",
    },
}

legend_font_sizes = {
    "small": {
        "titlesize": "16",
        "fontsize": "14",
    },
    "medium": {
        "titlesize": "20",
        "fontsize": "16",
    },
    "large": {
        "titlesize": "24",
        "fontsize": "20",
    },
}

## FILTER LEGAL VALUES
#     heuristic_modes_filter=[
#         mcts.NO_HEURISTIC,
#         # mcts.HEURISTIC_SELECT,
#     ],
#     selection_modes_filter=[
#         mcts.FULL_EXPAND,
#         # mcts.SQUARE_RATIO,
#     ],
#     loss_heuristics_filter=[
#         mcts.NO_HEURISTIC,
#         # mcts.FRAME_HEURISTIC,
#         # mcts.TOTAL_PLANT_COST_HEURISTIC,
#         # mcts.TOTAL_ZOMBIE_HP_HEURISTIC,
#         # mcts.ZOMBIES_LEFT_TO_SPAWN_HEURISTIC,
#     ],
#     expansion_modes_filter=[
#         mcts.NORMAL_MCTS,
#         # mcts.MAX_NODE,
#         # mcts.AVG_NODE,
#         # mcts.PARALLEL_TREES
#     ],


to_title = {
    "level": "Level",
    "time_ms": "Time (ms)",
    "threads": "Thread Count",
    "ucb_const": "UCB Const",
    "rollout_mode": "Parallelization Mode",
    "heuristic_mode": "Heuristic Mode",
    "selection_mode": "Selection Mode",
    "loss_heuristic": "Loss Heuristic",
    "win": "Win",
    "num_steps": "Amount of Steps",
}


def filter_pvz_data(
    df: pd.DataFrame,
    level: List[str] = None,
    time_ms_filter: Dict[str, int] = None,
    threads_filter: List[int] = None,
    ucb_filter: List[int] = None,
    heuristic_modes_filter: List[str] = None,
    selection_modes_filter: List[str] = None,
    loss_heuristics_filter: List[str] = None,
    expansion_modes_filter: List[str] = None,
):
    # Define filter conditions
    level_filter = (df["level"].isin(level)) if level else True
    ucb_value_filter = (df["ucb_const"].isin(ucb_filter)) if ucb_filter else True
    max_time_ms_filter = (df["time_ms"] <= time_ms_filter.get("max", math.inf)) if time_ms_filter else True
    min_time_ms_filter = time_ms_filter.get("min", 0) <= df["time_ms"] if time_ms_filter else True
    thread_filter = (df["threads"].isin(threads_filter)) if threads_filter else True
    heuristic_mode_filter = (df["heuristic_mode"].isin(heuristic_modes_filter)) if heuristic_modes_filter else True
    selection_mode_filter = (df["selection_mode"].isin(selection_modes_filter)) if selection_modes_filter else True
    loss_heuristic_filter = (df["loss_heuristic"].isin(loss_heuristics_filter)) if loss_heuristics_filter else True
    expansion_mode_filter = (df["rollout_mode"].isin(expansion_modes_filter)) if expansion_modes_filter else True

    # Apply filters
    filtered_data = df[
        level_filter
        & ucb_value_filter
        & max_time_ms_filter
        & min_time_ms_filter
        & thread_filter
        & heuristic_mode_filter
        & selection_mode_filter
        & loss_heuristic_filter
        & expansion_mode_filter
    ]

    return filtered_data


def plot_pvz_data(
    filtered_data: str,
    x_axis: str,
    y_axis: str = "win",
    title: str = None,
    file_name: str = None,
    log_scale: bool = False,
    # Different graphs by the value below
    group_graphs_by: str = "level",
    ylim: Tuple[int] = (0, 1),
    # Legend tuning...
    hue_order: List[Union[int, str]] = None,
    legend_location: str = "upper left",
    legend_size: str = "medium"
    # hue_norm=None,
):
    # Create a single plot
    plt.figure(figsize=(10, 6))

    ax = sns.lineplot(
        data=filtered_data,
        x=x_axis,
        y=y_axis,
        hue=group_graphs_by,
        marker="o",
        markersize=8,
        errorbar=None,
        sort=True,
        hue_order=hue_order,
        palette="colorblind",
    )

    if title is None:
        title = f"{x_axis} vs {y_axis}"

    plt.title(title, fontsize=20)
    plt.xlabel(x_axis, fontsize=14)
    plt.ylabel(y_axis, fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)

    # Get unique values for the legend based on group_graphs_by
    unique_legend_values = sorted(filtered_data[group_graphs_by].unique())

    if group_graphs_by in to_legend.keys():
        # Modify legend labels as needed
        legend_labels = [to_legend[group_graphs_by][value] for value in unique_legend_values]
    else:
        # Keep legend labels as-is
        legend_labels = unique_legend_values

    plt.legend(
        title=to_title[group_graphs_by],
        title_fontsize=legend_font_sizes[legend_size]["titlesize"],
        fontsize=legend_font_sizes[legend_size]["fontsize"],
        loc=legend_location,
        labels=legend_labels,
    )
    # Annotate each point with the correct sample count
    for line in ax.lines:
        x, y = line.get_xydata().T
        for xi, yi in zip(x, y):
            sample_count = len(filtered_data[(filtered_data[x_axis] == xi)])
            plt.text(xi, yi, sample_count, fontsize=8, ha="center", va="bottom", color="black")

    # Set to log scale if need be
    if log_scale:
        plt.xscale("log")

    if y_axis == "win" and ylim:
        plt.ylim(ylim)

    # Save the plot
    plt.tight_layout()
    plt.savefig(f"graphs/{file_name if file_name else title}.png")
    plt.show()


def filter_and_plot_pvz_data(
    data_path: str,
    x_axis: str,
    y_axis: str = "win",
    title: str = None,
    file_name: str = None,
    log_scale: bool = False,
    # Filters
    level: List[str] = None,
    time_ms_filter: Dict[str, int] = None,
    threads_filter: List[int] = None,
    ucb_filter: List[int] = None,
    heuristic_modes_filter: List[str] = None,
    selection_modes_filter: List[str] = None,
    loss_heuristics_filter: List[str] = None,
    expansion_modes_filter: List[str] = None,
    # Different graphs by the value below
    group_graphs_by: str = "level",
    ylim: Tuple[int] = (0, 1),
    # Legend tuning...
    hue_order: List[Union[int, str]] = None,
    legend_location: str = "upper left",
    legend_size: str = "medium"
    # hue_norm=None,
):
    # Read CSV file into a DataFrame
    df = pd.read_csv(data_path)
    filtered_data = filter_pvz_data(
        df,
        level,
        time_ms_filter,
        threads_filter,
        ucb_filter,
        heuristic_modes_filter,
        selection_modes_filter,
        loss_heuristics_filter,
        expansion_modes_filter,
    )
    plot_pvz_data(
        filtered_data,
        x_axis,
        y_axis,
        title,
        file_name,
        log_scale,
        group_graphs_by,
        ylim,
        hue_order,
        legend_location,
        legend_size,
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
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
    title="Normal Agent vs. Parallel-Max on Level 9+",
    file_name="6.1.1.2_level_9+_normal_vs_parallel_max",
    group_graphs_by="rollout_mode",
    legend_location="upper left",
)


# 6.1.1.2 ++
data_6_1_1_2 = filter_pvz_data(data_6_1_1, level=["9+"], threads_filter=None, expansion_modes_filter=[mcts.MAX_NODE])

plot_pvz_data(
    data_6_1_1_2,
    x_axis="time_ms",
    title="Varying Threads Parallel-Max on Level 9+",
    file_name="6.1.1.2_level_9+_parallel_max_threads",
    group_graphs_by="threads",
    legend_location="lower right",
)


# 6.1.1.3
data_6_1_1_3 = filter_pvz_data(data_6_1_1, level=["9++"], threads_filter=[8])

plot_pvz_data(
    data_6_1_1_3,
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
    title="Normal Agent vs. Parallel-Max vs. Parallel-Trees on Level 9+",
    file_name="6.1.2.2_level_9+_parallelizations",
    group_graphs_by="rollout_mode",
    legend_location="center right",
)


# 6.1.2.3
data_6_1_2_3 = filter_pvz_data(data_6_1_2, level=["9++"])

plot_pvz_data(
    data_6_1_2_3,
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
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
    x_axis="time_ms",
    group_graphs_by="loss_heuristic",
    legend_location="upper left",
    ylim=(0, 0.5),
)
