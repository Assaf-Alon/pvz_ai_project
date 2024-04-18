import pandas


data = pandas.read_csv("data/all.csv")


def filter_data(
    data,
    level=None,
    time_ms_filter={"min": 0, "max": 1000000},
    threads_filter=8,
    ucb_filter=None,
    heuristic_modes_filter=None,
    selection_modes_filter=None,
    loss_heuristics_filter=None,
    expansion_modes_filter=None,
):
    filtered_data = data  # type: pandas.DataFrame
    if level:
        filtered_data = filtered_data[filtered_data["level"].isin(level)]
    if time_ms_filter:
        filtered_data = filtered_data[
            (filtered_data["time_ms"] >= time_ms_filter["min"])
            & (filtered_data["time_ms"] <= time_ms_filter["max"])
        ]
    if threads_filter:
        filtered_data = filtered_data[filtered_data["threads"].isin(threads_filter)]
    if ucb_filter:
        filtered_data = filtered_data[filtered_data["ucb"].isin(ucb_filter)]
    if heuristic_modes_filter:
        filtered_data = filtered_data[
            filtered_data["heuristic_mode"].isin(heuristic_modes_filter)
        ]
    if selection_modes_filter:
        filtered_data = filtered_data[
            filtered_data["selection_mode"].isin(selection_modes_filter)
        ]
    if loss_heuristics_filter:
        filtered_data = filtered_data[
            filtered_data["loss_heuristic"].isin(loss_heuristics_filter)
        ]
    if expansion_modes_filter:
        filtered_data = filtered_data[
            filtered_data["expansion_mode"].isin(expansion_modes_filter)
        ]
    return filtered_data


def group_data(data: pandas.DataFrame, group_by):
    # drop values which contain less than 100 data points
    data = data.groupby(group_by).filter(lambda x: len(x) > 100)
    return data.groupby(group_by)


def generate_table():
    # generate a table which compares:
    # for each level, using each combination of heuristic, selection, loss, and expansion mode, for each ucb and for each time ms
    # the win rate, number of games played
    # generate the table in MD format
    # rollout_mode,heuristic_mode,selection_mode,loss_heuristic
    rollout_mode = [...]
    heuristic_mode = [...]
    selection_mode = [...]
    loss_heuristic = [...]

    table = "| Level | UCB | Time (ms) | Threads | Heuristic Mode | Selection Mode | Loss Heuristic | Expansion Mode | Win Rate | Games Played |\n"
    table += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    for level in ["1-1", "1-2", "1-3", "1-4", "1-5", "1-6", "1-7", "1-8", "1-9", "1-10"]:
        for r_mode in 

    print(table)