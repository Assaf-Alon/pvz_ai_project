import math
from build import level
from build import mcts
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# from scipy.interpolate import make_interp_spline, CubicSpline, BSpline
# import scipy.stats as st
from pprint import pprint
from time import time
import json
import csv

NORMAL_MCTS = mcts.NORMAL_MCTS
MAX_NODE = mcts.MAX_NODE
AVG_NODE = mcts.AVG_NODE
PARALLEL_TREES = mcts.PARALLEL_TREES

NO_HEURISTIC = mcts.NO_HEURISTIC
# HEURISTIC_MCTS = mcts.HEURISTIC_MCTS
HEURISTIC_SELECT = mcts.HEURISTIC_SELECT
# HEURISTIC_EXPAND = mcts.HEURISTIC_EXPAND


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
#         # mcts.NORMAL_MCTS,
#         # mcts.MAX_NODE,
#         # mcts.AVG_NODE,
#         mcts.PARALLEL_TREES
#     ],


rollout_mode_to_name = {
    NORMAL_MCTS: "No Parallelization",
    MAX_NODE: "Parallel MAX",
    AVG_NODE: "Parallel AVG",
    PARALLEL_TREES: "Parallel Trees",
}
heuristic_mode_to_name = {
    NO_HEURISTIC: "No Heuristic",
    # HEURISTIC_MCTS: "full heuristic",
    # HEURISTIC_EXPAND: "expand heuristic",
    HEURISTIC_SELECT: "Select Heuristic",
}

to_title = {
    "level": "Level",
    "time_ms": "Time (ms)",
    "threads": "Threads Count",
    "ucb_const": "UCB Const",
    "rollout_mode": "Parallelization Mode",
    "heuristic_mode": "Heuristic Mode",
    "selection_mode": "Selection Mode",
    "loss_heuristic": "Loss Heuristic",
    "win": "Win",
    "num_steps": "Amount of Steps",
}

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def filter_and_plot_pvz_data(
    data_path,
    x_axis,
    y_axis,
    title=None,
    file_name=None,
    log_scale=False,
    # Filters
    level=None,
    time_ms_filter=None,
    threads_filter=None,
    ucb_filter=None,
    heuristic_modes_filter=None,
    selection_modes_filter=None,
    loss_heuristics_filter=None,
    expansion_modes_filter=None,
    # Different graphs by the value below
    group_graphs_by="level",
    ylim=(0, 1),
    # Legend tuning...
    hue_order=None,
    legend_location="upper left",
    legend_size="medium"
    # hue_norm=None,
):
    # Read CSV file into a DataFrame
    df = pd.read_csv(data_path)

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


# def filter_data(
#     df,
#     level=None,
#     max_time_ms=None,
#     threads=None,
#     ucb_const=None,
#     heuristic_mode=None,
#     selection_mode=None,
#     loss_heuristic=None,
#     expansion_mode=None,
# ):
#     level_filter = (df["level"].isin(level)) if level else True
#     ucb_value_filter = (df["ucb_const"].isin(ucb_const)) if ucb_const else np.array([True] * len(df["ucb_const"]))
#     time_ms_filter = (df["time_ms"] <= max_time_ms) if max_time_ms else True
#     thread_filter = (df["threads"].isin(threads)) if threads else True
#     heuristic_mode_filter = (df["heuristic_mode"].isin(heuristic_mode)) if heuristic_mode else True
#     selection_mode_filter = (df["selection_mode"].isin(selection_mode)) if selection_mode else True
#     loss_heuristic_filter = (df["loss_heuristic"].isin(loss_heuristic)) if loss_heuristic else True
#     expansion_mode_filter = (df["rollout_mode"].isin(expansion_mode)) if expansion_mode else True

#     return df[
#         level_filter
#         & ucb_value_filter
#         & time_ms_filter
#         & thread_filter
#         & heuristic_mode_filter
#         & selection_mode_filter
#         & loss_heuristic_filter
#         & expansion_mode_filter
#     ]


# def group_and_plot_pvz_data(
#     filtered_data,
#     x_axis="time_ms",
#     y_axis="win",
#     title=None,
#     file_name=None,
#     grouping_rules=None,
#     # Legend tuning...
#     hue_order=None,
#     # hue_norm=None,
# ):
#     if grouping_rules is None:
#         raise ValueError("Please provide grouping rules.")

#     plt.figure(figsize=(10, 6))

#     for group_name, group_rules in grouping_rules.items():
#         group_filtered_data = filtered_data.copy()
#         if "level" in group_rules:
#             # Automatically group by all different available levels
#             group_filtered_data = group_filtered_data[
#                 group_filtered_data["level"].isin(group_filtered_data["level"].unique())
#             ]
#         else:
#             for rule_name, rule_values in group_rules.items():
#                 group_filtered_data = filter_data(group_filtered_data, **{rule_name: rule_values})

#         ax = sns.lineplot(
#             data=group_filtered_data,
#             x=x_axis,
#             y=y_axis,
#             hue="level",
#             marker="o",
#             markersize=8,
#             errorbar=None,
#             sort=True,
#             hue_order=hue_order,
#             palette="colorblind",
#         )

#         if title is None:
#             title = f"{x_axis} vs {y_axis}"

#         plt.title(f"{title} - {group_name}", fontsize=20)
#         plt.xlabel(x_axis, fontsize=16)
#         plt.ylabel(y_axis, fontsize=16)
#         plt.xticks(fontsize=14)
#         plt.yticks(fontsize=14)
#         plt.grid(True)
#         plt.legend(title="Level", title_fontsize="24", fontsize="20", loc="lower right")

#         # Annotate each point with the sample count
#         for line in ax.lines:
#             x, y = line.get_xydata().T
#             for xi, yi in zip(x, y):
#                 sample_count = len(group_filtered_data[group_filtered_data[x_axis] == xi])
#                 plt.text(xi, yi, sample_count, fontsize=8, ha="center", va="bottom", color="black")

#         # Save the plot
#         plt.tight_layout()
#         plt.savefig(f"graphs/{file_name if file_name else title}_{group_name}.png")
#         plt.show()


# all_data = pd.read_csv(CSV_FILENAME)

# basic_filters = {
#     "max_time_ms": 1600,
#     "ucb_const": [0.004],
#     "threads": None,
#     "heuristic_mode": [mcts.NO_HEURISTIC],
#     "selection_mode": [mcts.FULL_EXPAND],
#     "loss_heuristic": [mcts.NO_HEURISTIC],
#     "expansion_mode": [mcts.NORMAL_MCTS],
# }
# # 5.5.1
# filtered_data_5_5_1 = filter_data(df=all_data, level=["2", "4", "6", "7", "9"], **basic_filters)

# group_and_plot_pvz_data(
#     filtered_data_5_5_1,
#     title="Wins vs. Time for different levels",
#     file_name="5.5.1",
#     grouping_rules={"easy_levels": {"level": None}},
#     hue_order=["2", "4", "6", "7", "9"],
# )


# # 5.5.2.1
# filter_5_5_2_1 = basic_filters.copy()
# del filter_5_5_2_1["ucb_const"]
# filtered_data_5_5_2_1 = filter_data(df=all_data, level=["9"], **filter_5_5_2_1)

# group_and_plot_pvz_data(
#     filtered_data_5_5_2_1,
#     title="Wins vs. Time for different UCBs on Level 9",
#     file_name="5.5.2.1_level_9",
#     grouping_rules={"different_ucb": {"ucb_const": None}},
# )


############################################


# 5.5.1
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Wins vs. Time for different UCBs on Level 9",
    file_name="5.5.1_easy_levels",
    level=["1", "2", "4", "6", "7", "9"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="level",
    legend_location="lower right",
    legend_size="large",
)


# 5.5.2.1
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Wins vs. Time for different UCBs on Level 9",
    file_name="5.5.2.1_level_9_different_ucb",
    level=["9"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="ucb_const",
    legend_location="lower right",
)

# 5.5.2.2
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Wins vs. Time for different UCBs on Level 9+",
    file_name="5.5.2.2_level_9+_different_ucb",
    level=["9+"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="ucb_const",
    ylim=(0, 0.5),  # <----
)


# 5.5.2.3
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Wins vs. Time for different UCBs on Level 9+",
    file_name="5.5.2.3_level_9+_different_ucb_parallel_trees",
    level=["9+"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.PARALLEL_TREES],  # <--
    x_axis="ucb_const",  # <--
    y_axis="win",
    group_graphs_by="time_ms",  # <--
    log_scale=True,  # <--
    legend_location="upper right",
)


# 5.5.2.4
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Wins vs. Time for different UCBs on Level 9+",
    file_name="5.5.2.4_level_9+_different_ucb_parallel_trees_long_times",
    level=["9+"],
    time_ms_filter={"min": 1600},  # <--
    ucb_filter=[0.001, 0.004, 0.016, 0.064, 0.256, 1.024],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.PARALLEL_TREES],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="ucb_const",
    legend_location="lower right",
)


# 6.1.1.1
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Agent vs. Parallel-Max on Level 9",
    file_name="6.1.1.1_level_9_normal_vs_parallel_max",
    level=["9"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="rollout_mode",
    legend_location="lower right",
)

# 6.1.1.2
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Agent vs. Parallel-Max on Level 9+",
    file_name="6.1.1.2_level_9+_normal_vs_parallel_max",
    level=["9+"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.004],
    threads_filter=[8],  # <----
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="rollout_mode",
    legend_location="upper left",
)

# 6.1.1.2 ++
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Varying Threads Parallel-Max on Level 9+",
    file_name="6.1.1.2_level_9+_parallel_max_threads",
    level=["9+"],
    time_ms_filter={"max": 1600},
    ucb_filter=[0.004],
    threads_filter=None,
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.MAX_NODE],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="threads",
    legend_location="lower right",
)


# 6.1.1.3
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Agent vs. Parallel-Max on Level 9++",
    file_name="6.1.1.3_level_9++_normal_vs_parallel_max",
    level=["9++"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=[8],  # <----
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="rollout_mode",
    legend_location="upper left",
)

# 6.1.2.1
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Agent vs. Parallel-Max vs. Parallel-Trees on Level 9",
    file_name="6.1.2.1_level_9_parallelizations",
    level=["9"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=[8],  # <----
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.PARALLEL_TREES],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="rollout_mode",
    legend_location="lower right",
    ylim=(0, 1.02),  # Emphasis on 100%
)


# 6.1.2.2
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Agent vs. Parallel-Max vs. Parallel-Trees on Level 9+",
    file_name="6.1.2.2_level_9+_parallelizations",
    level=["9+"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=[8],
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.PARALLEL_TREES],
    x_axis="time_ms",
    y_axis="win",
    group_graphs_by="rollout_mode",
    legend_location="center right",
)


# 6.1.2.3
filter_and_plot_pvz_data(
    CSV_FILENAME,
    title="Normal Agent vs. Parallel-Max vs. Parallel-Trees on Level 9++",
    file_name="6.1.2.3_level_9++_parallelizations",
    level=["9++"],
    time_ms_filter={"max": 1600},  # <--
    ucb_filter=[0.004],
    threads_filter=[8],
    heuristic_modes_filter=[mcts.NO_HEURISTIC],
    selection_modes_filter=[mcts.FULL_EXPAND],
    loss_heuristics_filter=[mcts.NO_HEURISTIC],
    expansion_modes_filter=[mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.PARALLEL_TREES],
    x_axis="time_ms",
    y_axis="win",
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
    y_axis="win",
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
    y_axis="win",
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
    y_axis="win",
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
    y_axis="win",
    group_graphs_by="loss_heuristic",
    legend_location="upper left",
    ylim=(0, 0.5),
)


# filter_and_plot_pvz_data(
#     CSV_FILENAME,
#     level=["9+", "9++"],
#     max_time_ms_filter=1600,
#     ucb_filter=[0.004],
#     # threads_filter=None,
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
#         # mcts.NORMAL_MCTS,
#         # mcts.MAX_NODE,
#         # mcts.AVG_NODE,
#         mcts.PARALLEL_TREES
#     ],
#     x_axis="time_ms",
#     y_axis="win",
#     group_graphs_by="level"
# )
