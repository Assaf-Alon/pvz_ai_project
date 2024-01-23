from collections import defaultdict
import math
from typing import Dict, List, Tuple, Union
from build import mcts
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

to_legend_content = {
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


to_legend_title = defaultdict(lambda: lambda x: str(x))
to_legend_title.update(
    {
        "level": "Level",
        "time_ms": "Time (ms)",
        "threads": "Thread Count",
        "ucb_const": "UCB Const",
        "rollout_mode": "Parallelization Mode",
        "heuristic_mode": "Heuristic Mode",
        "selection_mode": "Selection Mode",
        "loss_heuristic": "Loss Heuristic",
        "win": "Win Percentage",
        "num_steps": "Amount of Steps",
        "name_in_legend": "Agent Description",
    }
)


def get_legend_title(feature: str):
    return to_legend_title.get(feature, feature)


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
    x_axis: str = "time_ms",
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
    legend_size: str = "medium",
    sort_legend: str = True,
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
    plt.xlabel(to_legend_title[x_axis], fontsize=16)
    plt.ylabel(to_legend_title[y_axis], fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)

    # Get unique values for the legend based on group_graphs_by
    unique_legend_values = filtered_data[group_graphs_by].unique()
    if sort_legend:
        unique_legend_values = sorted(unique_legend_values)

    if group_graphs_by in to_legend_content.keys():
        # Modify legend labels as needed
        legend_labels = [to_legend_content[group_graphs_by][value] for value in unique_legend_values]
    else:
        # Keep legend labels as-is
        legend_labels = unique_legend_values

    plt.legend(
        title=get_legend_title(group_graphs_by),
        title_fontsize=legend_font_sizes[legend_size]["titlesize"],
        fontsize=legend_font_sizes[legend_size]["fontsize"],
        loc=legend_location,
        labels=legend_labels,
    )
    # Annotate each point with the correct sample count
    for i in range(len(unique_legend_values)):
        line = ax.lines[i]
        x, y = line.get_xydata().T
        for xi, yi in zip(x, y):
            sample_count = len(
                filtered_data[
                    (filtered_data[x_axis] == xi) & (filtered_data[group_graphs_by] == unique_legend_values[i])
                ]
            )
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
    x_axis: str = "time_ms",
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
