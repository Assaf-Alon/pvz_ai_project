import pandas as pd
from statsmodels.stats.proportion import proportion_confint
import numpy as np
from pprint import pprint
from statsmodels.stats.power import NormalIndPower
import seaborn as sns
import matplotlib.pyplot as plt
from mcts import mcts


col_to_name = {
    "level": "Level",
    "time_ms": "Time (ms)",
    "threads": "Thread Count",
    "ucb_const": "UCB Const",
    "rollout_mode": "Parallelization Mode",
    "heuristic_mode": "Heuristic Mode",
    "selection_mode": "Selection Mode",
    "loss_heuristic": "Loss Heuristic",
    "win_rate": "Win Percentage",
    "num_steps": "Amount of Steps",
    "name_in_legend": "Agent Description",
}

# data = pd.read_csv("data/all.csv", dtype={"level": str, "time_ms": int, "rollout_mode": int, "heuristic_mode": int, "selection_mode": int, "loss_heuristic": int, "ucb_const": float, "win": bool})
# data = pd.read_csv("data/all.csv")


def get_sample_thershold():
    effect_size = 0.2  # desired effect size
    alpha = 0.05  # significance level
    power = 0.8  # desired power

    # Perform power analysis
    nobs = NormalIndPower().solve_power(effect_size=effect_size, alpha=alpha, power=power, alternative='two-sided')

    print("Number of observations needed:", round(nobs))
    return round(nobs)

def create_cleaned_csv():
    # transform names of values in columns rollout_mode, heuristic_mode, selection_mode, loss_heuristic
    data = pd.read_csv("data/all.csv")
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
        mcts.TOTAL_PLANT_COST_HEURISTIC: "total plant cost"
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
    data["selection_mode"] = data["selection_mode"].map(selection_mode_to_name)
    data["loss_heuristic"] = data["loss_heuristic"].map(loss_heuristic_to_name)
    data["rollout_mode"] = data["rollout_mode"].map(rollout_mode_to_name)
    data["heuristic_mode"] = data["heuristic_mode"].map(heuristic_mode_to_name)
    # aggregate data
    data = data.groupby(["level", "time_ms", "rollout_mode", "heuristic_mode", "selection_mode", "loss_heuristic", "ucb_const", "threads"]).agg(
        num_games=("win", "count"),
        num_wins=("win", "sum")
    )
    data.reset_index(inplace=True)
    data["win_rate"] = data["num_wins"] / data["num_games"]
    data["lower_bound"], data["upper_bound"] = zip(*data.apply(lambda row: proportion_confint(row["num_wins"], row["num_games"], alpha=0.05, method='wilson') if row["num_games"] > 0 else (np.nan, np.nan), axis=1))
    data["lower_bound"] = data["lower_bound"].apply(lambda x: round(x, 2) if not np.isnan(x) else np.nan)
    data["upper_bound"] = data["upper_bound"].apply(lambda x: round(x, 2) if not np.isnan(x) else np.nan)
    data = data[data["num_games"] > 200]
    data.to_csv("data/cleaned.csv", index=False)


class Line():
    def __init__(self, level, rollout_mode = None, heuristic_mode = None, selection_mode = None, loss_heuristic = None, ucb_const = None, time_ms = None, threads=8):
        self.level = level
        self.rollout_mode = rollout_mode
        self.heuristic_mode = heuristic_mode
        self.selection_mode = selection_mode
        self.loss_heuristic = loss_heuristic
        self.ucb_const = ucb_const
        self.time_ms = time_ms
        self.threads = threads

    def filter_data(self, data: pd.DataFrame):
        data = data.copy()
        data = data[data["level"] == self.level]
        if self.rollout_mode:
            data = data[data["rollout_mode"] == self.rollout_mode]
        if self.heuristic_mode:
            data = data[data["heuristic_mode"] == self.heuristic_mode]
        if self.selection_mode:
            data = data[data["selection_mode"] == self.selection_mode]
        if self.loss_heuristic:
            data = data[data["loss_heuristic"] == self.loss_heuristic]
        if self.ucb_const:
            data = data[data["ucb_const"] == self.ucb_const]
        if self.time_ms:
            data = data[data["time_ms"] == self.time_ms]
        if self.threads:
            data = data[data["threads"] == self.threads]
        return data
    
    def get_legend_dict(self):
        legend_dict = {}
        legend_dict["level"] = self.level
        if self.rollout_mode:
            legend_dict["rollout_mode"] = self.rollout_mode
        if self.heuristic_mode:
            legend_dict["heuristic_mode"] = self.heuristic_mode
        if self.selection_mode:
            legend_dict["selection_mode"] = self.selection_mode
        if self.loss_heuristic:
            legend_dict["loss_heuristic"] = self.loss_heuristic
        if self.ucb_const:
            legend_dict["ucb_const"] = self.ucb_const
        if self.time_ms:
            legend_dict["time_ms"] = self.time_ms
        return legend_dict
    
    def get_legend(self, labels):
        legend_dict = self.get_legend_dict()
        legend = " ".join([f"{label}: {legend_dict[label]}," for label in labels])
        legend = legend[:-1]
        return legend

def create_graph(x_axis, y_axis, line_list: list[Line], title: str, labels, **kwargs):
    global full_data
    data = full_data.copy()

    if "time_ms_range" in kwargs:
        data = data[data["time_ms"].between(kwargs["time_ms_range"][0], kwargs["time_ms_range"][1])]

    # plot lines using sns.scatterplot
    sns.set_theme()
    sns.set_context("paper")
    fig, ax = plt.subplots()
    for line in line_list:
        line_data = line.filter_data(data)
        line_data.sort_values(by=x_axis, inplace=True)
        line_label = line.get_legend(labels)
        sns.lineplot(data=line_data, x=x_axis, y=y_axis, ax=ax, label=line_label, marker="o")
        ci_lower = line_data["lower_bound"]
        ci_upper = line_data["upper_bound"]
        ax.fill_between(line_data[x_axis], ci_lower, ci_upper, color='b', alpha=.1)
    
    plt.xlabel(col_to_name[x_axis])
    plt.ylabel(col_to_name[y_axis])
    plt.title(title)
    if x_axis in ["ucb_const"]:
        plt.xscale("log")

    fig.set_size_inches(fig.get_size_inches() * 1.5)
    plt.tight_layout()

    plt.savefig(f"dgershko_graphs/{title.replace(" ", "_")}.png")


if __name__ == "__main__":
    # create_cleaned_csv()

    full_data = pd.read_csv("data/cleaned.csv")
    full_data = full_data[full_data["time_ms"] < 3200]
    full_data = full_data[full_data["num_games"] > 200]
    
    # graph for comparing base agent on different levels
    lines = []
    for level in [str(level) for level in range(1, 10)] + ["9+", "9++"]:
        line = Line(level, rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004)
        lines.append(line)
    title = "Base Agent Performence on Different Levels"
    create_graph("time_ms", "win_rate", lines, title, ["level"])

    # graph for comparing ucb constants in the base agent
    lines = []
    lines.append(Line("9", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=200))
    lines.append(Line("9", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=800))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=200))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=800))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=200))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=800))
    title = "Agent Performence on Different UCB Constants"
    create_graph("ucb_const", "win_rate", lines, title, ["level", "time_ms"])

    # graphs for comparing rollout strategies
    lines = []
    lines.append(Line("9", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "Comparison of rollout strategies on level 9"
    create_graph("time_ms", "win_rate", lines, title, ["rollout_mode"], time_ms_range=[100, 700])

    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "Comparison of rollout strategies on level 9+"
    create_graph("time_ms", "win_rate", lines, title, ["rollout_mode"])

    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "Comparison of rollout strategies on level 9++"
    create_graph("time_ms", "win_rate", lines, title, ["rollout_mode"])

    # graph for comparing selection strategies in different rollout strategies
    # level 9
    lines = []
    lines.append(Line("9", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "Comparison of selection strategies on level 9"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])
    # level 9+
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "Comparison of selection strategies on level 9+"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])
    # level 9++
    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "Comparison of selection strategies on level 9++"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])


    # graphs for comparing heuristics
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "Comparison of heuristics on level 9"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode", "selection_mode", "loss_heuristic"])