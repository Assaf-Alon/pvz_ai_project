import pandas as pd
from pprint import pprint
from tabulate import tabulate
import numpy as np
import scipy.stats as stats
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.power import NormalIndPower


pd.set_option('display.max_rows', None)

data = pd.read_csv("data/all.csv")

def generate_table():
    """
    Print statistics for each combination of parameters
    Separate by levels (for each unique level in the data)
    """
    
    for level in data["level"].unique():
        print(f"Level {level}")
        table = data[data["level"] == level].groupby(["rollout_mode", "heuristic_mode", "selection_mode", "loss_heuristic", "ucb_const", "time_ms"]).agg(
            num_games=("win", "count"),
            num_wins=("win", "sum")
        )
        table["win_rate"] = table["num_wins"] / table["num_games"]
        table["confidence_interval"] = table.apply(lambda row: proportion_confint(row["num_wins"], row["num_games"], alpha=0.05, method='wilson') if row["num_games"] > 0 else (np.nan, np.nan), axis=1)
        table["confidence_interval"] = table["confidence_interval"].apply(lambda ci: f"[{ci[0]:.2f}, {ci[1]:.2f}]" if not np.isnan(ci[0]) else "N/A")
        print(tabulate(table, headers='keys', tablefmt='fancy_grid'))
        print("\n\n\n")


def get_sparse_params(min_sample_size: int):
    table = data.groupby(["level", "rollout_mode", "heuristic_mode", "selection_mode", "loss_heuristic", "ucb_const", "time_ms"]).agg(
        num_games=("win", "count"),
        win_rate=("win", "mean")
    )
    # for each combination of parameters which has less than 100 games played, save the parameters to a list
    sparse_params = table[table["num_games"] < min_sample_size].reset_index().values.tolist()
    # remove the last two columns
    sparse_params = [x[:-1] for x in sparse_params]
    # add column for number of games played
    sparse_params_df = pd.DataFrame(sparse_params)
    # add header to the csv"
    sparse_params_df.columns = ["level", "rollout_mode", "heuristic_mode", "selection_mode", "loss_heuristic", "ucb_const", "time_ms", "num_games"]
    sparse_params_df.to_csv("data/sparse_params.csv", index=False)


def get_sample_thershold():
    effect_size = 0.2  # desired effect size
    alpha = 0.05  # significance level
    power = 0.8  # desired power

    # Perform power analysis
    nobs = NormalIndPower().solve_power(effect_size=effect_size, alpha=alpha, power=power, alternative='two-sided')

    print("Number of observations needed:", round(nobs))
    return round(nobs)


def generate_statistical_csv(sample_size_threshold: int):
    for level in data["level"].unique():
        table = data[data["level"] == level].groupby(["rollout_mode", "heuristic_mode", "selection_mode", "loss_heuristic", "ucb_const", "time_ms"]).agg(
            num_games=("win", "count"),
            num_wins=("win", "sum")
        )
        # filter out rows with less than the sample size threshold
        table = table[table["num_games"] >= sample_size_threshold]
        table["win_rate"] = table["num_wins"] / table["num_games"]
        table["confidence_interval"] = table.apply(lambda row: proportion_confint(row["num_wins"], row["num_games"], alpha=0.05, method='wilson') if row["num_games"] > 0 else (np.nan, np.nan), axis=1)
        table["confidence_interval"] = table["confidence_interval"].apply(lambda ci: f"[{ci[0]:.2f}, {ci[1]:.2f}]" if not np.isnan(ci[0]) else "N/A")
        table.reset_index(inplace=True)
        table["level"] = level
        table.to_csv(f"data/{level}_statistical.csv", index=False)

if __name__ == "__main__":
    min_sample_size = get_sample_thershold()
    get_sparse_params(min_sample_size)
    generate_statistical_csv(min_sample_size)

