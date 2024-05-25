import pandas as pd
from statsmodels.stats.proportion import proportion_confint
import numpy as np
from pprint import pprint
from statsmodels.stats.power import NormalIndPower
import seaborn as sns
import matplotlib.pyplot as plt
from mcts import mcts
import os
# from config import *
import config as cfg

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
    data = pd.read_csv("data/all.csv", low_memory=False)
    data["selection_mode"] = data["selection_mode"].map(cfg.selection_mode_to_name)
    data["loss_heuristic"] = data["loss_heuristic"].map(cfg.loss_heuristic_to_name)
    data["rollout_mode"] = data["rollout_mode"].map(cfg.rollout_mode_to_name)
    data["heuristic_mode"] = data["heuristic_mode"].map(cfg.heuristic_mode_to_name)
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
    data = data[data["num_games"] > 10]
    data.to_csv("data/cleaned.csv", index=False)


def transform_csv_to_params(path):
    # reverse the transformation of names of values in columns rollout_mode, heuristic_mode, selection_mode, loss_heuristic
    data = pd.read_csv(path)
    data["selection_mode"] = data["selection_mode"].map(cfg.selection_mode_name_to_mode)
    data["loss_heuristic"] = data["loss_heuristic"].map(cfg.loss_heuristic_name_to_mode)
    data["rollout_mode"] = data["rollout_mode"].map(cfg.rollout_mode_name_to_mode)
    data["heuristic_mode"] = data["heuristic_mode"].map(cfg.heuristic_mode_name_to_mode)
    data.to_csv(path, index=False)



class Line():
    def __init__(self, level, rollout_mode = None, heuristic_mode = None, selection_mode = None, loss_heuristic = None, ucb_const = None, time_ms = None, threads=8, name_in_legend=None, save_params=False):
        self.level = level
        self.rollout_mode = rollout_mode
        self.heuristic_mode = heuristic_mode
        self.selection_mode = selection_mode
        self.loss_heuristic = loss_heuristic
        self.ucb_const = ucb_const
        self.time_ms = time_ms
        self.threads = threads
        self.name_in_legend = name_in_legend
        # self.save_params = save_params
        self.save_params = True
        
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
        if self.save_params:
            if not os.path.exists("data/graph_params.csv"):
                data.to_csv("data/graph_params.csv", index=False)
            else:
                data.to_csv("data/graph_params.csv", index=False, mode='a', header=False)
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
        if self.threads:
            legend_dict["threads"] = self.threads
        return legend_dict
    
    def get_legend(self, labels):
        if self.name_in_legend:
            return self.name_in_legend
        legend_dict = self.get_legend_dict()
        legend = " ".join([f"{label}: {legend_dict[label]}," for label in labels])
        legend = legend[:-1]
        return legend

# class Graph():
#     def __init__(self, lines: list[Line], x_axis, y_axis, title, labels, data, scaling_factor=None):
#         self.lines = lines
#         self.x_axis = x_axis
#         self.y_axis = y_axis
#         self.title = title
#         self.labels = labels
#         self.scaling_factor = scaling_factor
#         self.data = data
#         if "time_ms_range" in kwargs:
#             self.data = self.data[self.data["time_ms"].between(kwargs["time_ms_range"][0], kwargs["time_ms_range"][1])]
    
#     def draw(self):
        
        


def create_graph(x_axis, y_axis, line_list: list[Line], title: str, labels, **kwargs):
    """
    Create a graph with multiple lines using the provided data.

    Args:
        x_axis (str): The column name to be used as the x-axis.
        y_axis (str): The column name to be used as the y-axis.
        line_list (list[Line]): A list of Line objects representing the lines to be plotted.
        title (str): The title of the graph.
        labels: The labels to be used for the legend.
        **kwargs: Additional keyword arguments for customizing the graph.

    Keyword Args:
        time_ms_range (tuple): A tuple representing the range of time_ms values to be included in the graph.
        scaling_factor (float): A scaling factor to adjust the size of the graph.
    """
    global full_data
    data = full_data.copy()

    if "time_ms_range" in kwargs:
        data = data[data["time_ms"].between(kwargs["time_ms_range"][0], kwargs["time_ms_range"][1])]

    # plot lines using sns.scatterplot
    sns.set_theme()
    sns.set_context("talk")
    fig, ax = plt.subplots()
    for line in line_list:
        line_data = line.filter_data(data)
        line_data.sort_values(by=x_axis, inplace=True)
        line_label = line.get_legend(labels)
        sns.lineplot(data=line_data, x=x_axis, y=y_axis, ax=ax, label=line_label, marker="o")
        ci_lower = line_data["lower_bound"]
        ci_upper = line_data["upper_bound"]
        ax.fill_between(line_data[x_axis], ci_lower, ci_upper, color='b', alpha=.1)
        # print number of games for each point in each line
        
    
    plt.ylim(0, 1)
    plt.xlabel(col_to_name[x_axis])
    plt.ylabel(col_to_name[y_axis])
    plt.title(title)
    if x_axis in ["ucb_const"]:
        plt.xscale("log")

    if "scaling_factor" in kwargs:
        fig.set_size_inches(fig.get_size_inches() * kwargs["scaling_factor"])
    else:
        fig.set_size_inches(fig.get_size_inches() * 1.5) # default scaling factor
    plt.tight_layout()

    plt.savefig(f"dgershko_graphs/{title.replace(" ", "_")}.png")
    plt.close()

def generate_experiment_params():
    used_params = pd.read_csv("data/graph_params.csv")
    used_params = used_params.drop_duplicates()
    # sort by size of confidence interval
    used_params["ci_size"] = used_params["upper_bound"] - used_params["lower_bound"]
    # filter out the parameters that have a confidence interval size < 0.1
    used_params = used_params[used_params["ci_size"] >= 0.05]
    used_params.sort_values(by="ci_size", ascending=False, inplace=True)
    # transform param names to values
    used_params["selection_mode"] = used_params["selection_mode"].map(cfg.selection_mode_name_to_mode)
    used_params["loss_heuristic"] = used_params["loss_heuristic"].map(cfg.loss_heuristic_name_to_mode)
    used_params["rollout_mode"] = used_params["rollout_mode"].map(cfg.rollout_mode_name_to_mode)
    used_params["heuristic_mode"] = used_params["heuristic_mode"].map(cfg.heuristic_mode_name_to_mode)
    used_params.to_csv("data/experiment_params.csv", index=False)
    os.remove("data/graph_params.csv") # delete the graph params to avoid duplication of contents

if __name__ == "__main__":
    create_cleaned_csv()
    # delete all graphs in the folder
    import os
    folder = "dgershko_graphs"
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            os.remove(os.path.join(folder, filename))

    full_data = pd.read_csv("data/cleaned.csv")
    full_data = full_data[full_data["time_ms"] < 3200]
    full_data = full_data[full_data["num_games"] > 10]
    
    # graph for comparing base agent on different levels
    lines = []
    for level in [str(level) for level in range(1, 10)] + ["9+", "9++"]:
        line = Line(level, rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004)
        lines.append(line)
    title = "Base Agent Performence on Different Levels"
    create_graph("time_ms", "win_rate", lines, title, ["level"], scaling_factor=2)

    # general UCB comparison
    lines = []
    lines.append(Line("9", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=100))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=400))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=400))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=400))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", time_ms=400))
    title = "UCB Comparison for selected scenarios"
    create_graph("ucb_const", "win_rate", lines, title, ["level", "rollout_mode", "time_ms"], scaling_factor=2)

    # graphs for comparing rollout strategies
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "rollout strategies on level 9+"
    create_graph("time_ms", "win_rate", lines, title, ["rollout_mode"])

    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "rollout strategies on level 9++"
    create_graph("time_ms", "win_rate", lines, title, ["rollout_mode"])

    # graphs for comparing rollout strategies with different core counts in level 9+
    # level 9+ parallel max
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, name_in_legend="base agent"))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, threads=2))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, threads=4))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, threads=8))
    title = "parallel max on level 9+ with different core counts"
    create_graph("time_ms", "win_rate", lines, title, ["threads"])
    # level 9+ parallel trees
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, name_in_legend="base agent"))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, threads=2))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, threads=4))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, threads=8))
    title = "parallel trees on level 9+ with different core counts"
    create_graph("time_ms", "win_rate", lines, title, ["threads"])
    
    

    # graph for comparing selection strategies in different rollout strategies
    # level 9+ normal
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection strategies on level 9+ - normal agent"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])
    # level 9+ parallel max
    lines = []
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection strategies on level 9+ - parallel max agent"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])
    # level 9+ parallel trees
    lines = []
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection strategies on level 9+ - parallel trees agent"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])
    # level 9++ normal
    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection strategies on level 9++ - normal agent"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])
    # level 9++ parallel max
    lines = []
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection strategies on level 9++ - parallel max agent"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])
    # level 9++ parallel trees
    lines = []
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="square ratio", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection strategies on level 9++ - parallel trees agent"
    create_graph("time_ms", "win_rate", lines, title, ["selection_mode"])


    # graphs for comparing heuristics
    # level 9+ normal, different loss heuristics
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no_heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total zombie hp", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="zombies left to spawn", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="frame", ucb_const=0.004))
    title = "different loss heuristics on level 9+ - normal agent"
    create_graph("time_ms", "win_rate", lines, title, ["loss_heuristic"])
    # level 9+ normal selection
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection heuristic on level 9+"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode"], scaling_factor=1.3)
    # level 9++ normal selection
    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    title = "selection heuristic on level 9++"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode"], scaling_factor=1.3)
    # level 9+ normal loss
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "loss heuristic on level 9+ - normal agent"
    create_graph("time_ms", "win_rate", lines, title, ["loss_heuristic"], scaling_factor=1.3)
    # level 9++ normal loss
    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "loss heuristic on level 9++ - normal agent"
    create_graph("time_ms", "win_rate", lines, title, ["loss_heuristic"], scaling_factor=1.3)
    # level 9+ selection and loss
    lines = []
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "heuristics on level 9+ - normal agent"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode", "loss_heuristic"], scaling_factor=1.8)
    # level 9++ selection and loss
    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "heuristics on level 9++ - normal agent"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode", "loss_heuristic"], scaling_factor=1.8)
    # level 9+ parallel max
    lines = []
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel max", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "heuristics on level 9+ - parallel max"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode", "loss_heuristic"], scaling_factor=1.8)
    # level 9++ parallel max
    lines = []
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "heuristics on level 9++ - parallel max"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode", "loss_heuristic"], scaling_factor=1.8)
    # level 9+ parallel trees
    lines = []
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9+", rollout_mode="parallel trees", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "heuristics on level 9+ - parallel trees"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode", "loss_heuristic"], scaling_factor=1.8)
    # level 9++ parallel trees
    lines = []
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004))
    title = "heuristics on level 9++ - parallel trees"
    create_graph("time_ms", "win_rate", lines, title, ["heuristic_mode", "loss_heuristic"], scaling_factor=1.8)

    # compound improvements on level 9++
    lines = []
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, name_in_legend="base agent"))
    lines.append(Line("9++", rollout_mode="normal", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004, name_in_legend="heuristic improvement"))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, name_in_legend="parallel max"))
    lines.append(Line("9++", rollout_mode="parallel max", heuristic_mode="select heuristic", selection_mode="full expand", loss_heuristic="total plant cost", ucb_const=0.004, name_in_legend="parallel max + heuristic improvement"))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="no heuristic", selection_mode="full expand", loss_heuristic="no heuristic", ucb_const=0.004, name_in_legend="parallel trees"))
    lines.append(Line("9++", rollout_mode="parallel trees", heuristic_mode="select heuristic", selection_mode="square ratio", loss_heuristic="total plant cost", ucb_const=0.004, name_in_legend="parallel trees + heuristic improvement"))
    title = "compound improvements on level 9++"
    create_graph("time_ms", "win_rate", lines, title, ["name_in_legend"], scaling_factor=2.5)

    # generate_experiment_params()