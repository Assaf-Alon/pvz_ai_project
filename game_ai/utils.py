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


CSV_FILENAME = "data/data.csv"
plant_to_name = ("no_plant","cherrybomb","chomper","hypnoshroom","iceshroom","jalapeno","peashooter","potatomine","puffshroom","repeaterpea","scaredyshroom","snowpea","spikeweed","squash","sunflower","sunshroom","threepeater","wallnut")

def construct_level_data_from_list(list: list):
    list.sort(key=lambda item: item[0]) # sort by first element of tuple (list[tuple])
    level_data = level.ZombieQueue()
    for item in list:
        level_data.push_back(level.ZombieSpawnTemplate(item[0], item[1], item[2]))
    return level_data

def get_level_info(level_num: int):
    with open("data/levels.json", "r") as level_json:
        levels = json.load(level_json)
    level_info = levels[f"level_{level_num}"]
    zombie_list, plant_list = level_info["zombies"], level_info["plants"]
    return construct_level_data_from_list(zombie_list), plant_list

def get_numpy_arr_from_level_obs(level: level.Level):
    arr = level.get_observation()
    result = np.asarray(arr)
    return result

def print_level_state(level: level.Level):
    state = level.get_state() # type: level.State
    for lane in range(state.size()):
        for col in range(state[lane].size()):
            cell = state[lane][col] # type: level.Cell

def get_plants_from_observation(observation: np.ndarray):
    result = []
    num_rows, num_cols, _ = observation.shape
    for row in range(num_rows):
        for col in range(num_cols):
            plant_type, _, _ = observation[row][col]
            if plant_type != 0:
                result.append((plant_to_name[plant_type], row, col))
    return result

def get_frame_from_observation(observation: np.ndarray):
    num_rows, num_cols, _ = observation.shape

    # Create a blank frame
    frame = np.zeros((num_rows, num_cols * 2, 3))

    # Iterate over each cell in the observation
    for row in range(num_rows):
        for col in range(num_cols):
            plant_type, hp_thirds, zombie_danger = observation[row][col]

            # Calculate the color for the left half of the cell based on plant_type and hp_thirds
            if plant_type == 0:
                plant_pixel = [0, 0, 0]  # Black
            else:
                intensity = min(1.0, hp_thirds / 3.0)
                if plant_type in [level.SUNFLOWER, level.SUNSHROOM]: # producer plants are yellow 
                    plant_pixel = [intensity, intensity, 0]
                elif plant_type in [level.PEASHOOTER, level.THREEPEATER, level.REPEATERPEA]: # shooter plants are green
                    plant_pixel = [0, intensity, 0]
                elif plant_type in [level.WALLNUT]: # wall plants are blue
                    plant_pixel = [0, 0, intensity]
                else: # mine/special plants are purple
                    plant_pixel = [intensity, 0, intensity]

            # Calculate the color for the right half of the cell based on zombie_danger
            if zombie_danger != 0:
                right_color_intensity = min(1.0, zombie_danger / 3.0)
                zombie_pixel = [right_color_intensity, 0, 0]  # Shades of red based on zombie_danger
            else:
                zombie_pixel = plant_pixel

            # Set the colors for the left and right halves of the cell in the frame
            frame[row][col * 2] = plant_pixel
            frame[row][col * 2 + 1] = zombie_pixel

    return frame

def animate_observation_buffer(observation_buffer: list):
    fig, ax = plt.subplots()
    # text_annotation = ax.annotate("Plants", xy=(0.25, 0.95), xycoords="figure fraction", ha="center", va="center", wrap=True, bbox=dict(boxstyle="round", fc="w"))
    # Set up an initial plot with the first frame
    annotations = [] # type: list[plt.text.Annotation]
    im = ax.imshow(get_frame_from_observation(observation_buffer[0]))

    # Define the update function for the animation
    def update(frame):
        # print(frame)
        # Update the plot with the next frame
        im.set_array(get_frame_from_observation(observation_buffer[frame]))
        # text_annotation.set_text(f"Plants: {get_plants_from_observation(observation_buffer[frame])}")
        for annotation in annotations:
            annotation.remove()
        annotations.clear()
        for plant_name, row, col in get_plants_from_observation(observation_buffer[frame]):
            annotations.append(ax.annotate(plant_name, xy=(col * 2 + 0.5, row), xycoords="data", ha="center", va="center", wrap=True, bbox=dict(boxstyle="round", fc="w")))
        return im, *annotations
    # Create the animation object using the FuncAnimation class
    anim = animation.FuncAnimation(fig, update, frames=len(observation_buffer), interval=1, blit=True)
    num_cols = observation_buffer[0].shape[1] // 2
    num_rows = observation_buffer[0].shape[0]
    aspect_ratio = num_cols / observation_buffer[0].shape[0]
    plt.gca().set_aspect(2)

    # Set custom tick positions for half-width columns
    ax.set_xticks(np.arange(num_cols) * 2 + 0.5)
    ax.set_yticks(np.arange(observation_buffer[0].shape[0]) + 0.5)
    ax.set_xticklabels(list(range(num_cols)))
    ax.set_yticklabels(list(range(num_rows)))
    # Show the animation
    plt.show()

def run_animation():
    level = level.Level(5, 10, 10, get_level_info(1))
    frame_list = []
    while not level.done:
        level.step(level.get_random_action())
        obs = get_numpy_arr_from_level_obs(level)
        frame = get_frame_from_observation(obs)
        frame_list.append(frame)
    animate_observation_buffer(frame_list)

def simulate_set_game(level: level.Level, action_list: list[level.Action]):
    observations = []
    for action in action_list:
        while not level.is_action_legal(action) and not level.done:
            level.step()
            observation = np.asarray(level.get_observation())
            observations.append(observation)
        level.step(action)
    while not level.done:
        level.step()
        observation = np.asarray(level.get_observation())
        observations.append(observation)
    # print(f"lawnmowers: {level.lawnmowers[0]} {level.lawnmowers[1]} {level.lawnmowers[2]} {level.lawnmowers[3]} {level.lawnmowers[4]}")
    animate_observation_buffer(observations)
    print(f"game eneded with win: {level.win}")


def action_to_string(action: level.Action):
    return f"action: plant {plant_to_name[action.plant_name]} at coords: {action.lane}, {action.col}"
    
def estimate_simulation_speed():
    level = level.Level(5, 10, 10, get_level_info(1))
    num_rollout = 1000000
    start = time()
    level.rollout(14, num_rollout)
    end = time()
    print(f"total time: {end-start}, time per rollout: {(end-start)/num_rollout}")

def play_level1():
    FPS = 10
    GAMES = 10000
    env = level.Level(1, 10, FPS, *get_level_info(1))
    print(f"Level 1 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 1 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 1 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level2():
    FPS = 10
    GAMES = 10000
    env = level.Level(3, 10, FPS, *get_level_info(2))
    print(f"Level 2 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 2 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 2 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level3():
    FPS = 10
    GAMES = 10000
    env = level.Level(3, 10, FPS, *get_level_info(3))
    print(f"Level 3 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 3 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 3 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level4():
    FPS = 10
    GAMES = 10000
    env = level.Level(5, 10, FPS, *get_level_info(4))
    print(f"Level 4 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 4 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 4 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level9():
    FPS = 10
    GAMES = 10000
    env = level.Level(5, 10, FPS, *get_level_info(9))
    print(f"Level 9 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 9 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 9 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def csv_append(new_data: dict, filename=CSV_FILENAME):
    """
    CSV columns are:
    level, time_ms, threads, ucb_const, rollout_mode, win, num_steps
    NOTE: num_steps is the number of steps needed to achieve a state from which empty steps give a victory!!! set to -1 for losses.
    """
    data_csv = open(filename, "a+")
    data_writer = csv.writer(data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
    new_row = [new_data["level"], new_data["time_ms"], new_data["parallel_factor"], new_data["ucb_const"], new_data["rollout_mode"], new_data["heuristic_mode"], new_data["selection_mode"], new_data["win"], new_data["num_steps"]]
    data_writer.writerow(new_row)

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

def replace_data_mode_names(data):
    for index in range(len(data)):
        for key, value in data[index].items():
            if key == "rollout_mode":
                data[index][key] = rollout_mode_to_name[int(value)]
            elif key == "heuristic_mode":
                data[index][key] = heuristic_mode_to_name[int(value)]
    return data

def replace_filter_mode_names(filter_list):
    for filter_index in range(len(filter_list)):
        for index in range(len(filter_list[filter_index])):
            for key, value in filter_list[filter_index][index].items():
                if key == "rollout_mode":
                    filter_list[filter_index][index][key] = rollout_mode_to_name[int(value)]
                elif key == "heuristic_mode":
                    filter_list[filter_index][index][key] = heuristic_mode_to_name[int(value)]
    return filter_list

def test_generate_plot(csv_file, x_axis, y_axis, filter_list, log, graph):
    with open(csv_file, 'r') as csv_file_handle:
        data = list(csv.DictReader(csv_file_handle))

    data = replace_data_mode_names(data)
    filter_list = replace_filter_mode_names(filter_list)
    
    # create subplots by getting the sqrt of the number of filters
    num_rows = num_cols = int(np.ceil(np.sqrt(len(filter_list))))

    fig, axes = plt.subplots(num_rows, num_cols)

    manager = plt.get_current_fig_manager()
    manager.window.maximize()

    for fig_num, filters in enumerate(filter_list):
        for filter in filters:
            filtered_data = data.copy()
            # Filter data using filter dictionary
            for key, value in filter.items():
                filtered_data = [row for row in filtered_data if row[key] == str(value)]
            grouped_data = {}
            # Group data by x-axis
            for row in filtered_data:
                if row[x_axis] not in grouped_data:
                    grouped_data[row[x_axis]] = []
                if (row[y_axis] == "False" or row[y_axis] == "True"):
                    grouped_data[row[x_axis]].append(bool(row[y_axis] == "True"))
                else:
                    grouped_data[row[x_axis]].append(float(row[y_axis]))
            
            # Calculate mean of y-axis
            for key, value in grouped_data.items():
                grouped_data[key] = [sum([int(x) for x in value]) / len(value), len(value)]
                # conf_lower, conf_upper = st.norm.interval(0.9, loc=grouped_data[key][0], scale=st.sem(value))
                # print(f"lower bound: {conf_lower}, upper bound: {conf_upper}")

            # Sort data by x-axis
            sorted_keys = sorted(grouped_data.keys())
            sorted_data = [grouped_data[x][0] for x in sorted_keys]
            # lower and upper bounds for each data point, 95% confidence interval
            # sorted_error = np.array([st.norm.interval(0.95, loc=grouped_data[key][0], scale=st.sem(value)) for key in sorted_keys])
            # data points with error applied
            # error_data = np.array([sorted_data - sorted_error[:, 0], sorted_error[:, 1] - sorted_data])
            if (x_axis == "rollout_mode"):
                mode_to_name = {
                    "0": "normal",
                    "1": "parallel max",
                    "2": "parallel avg",
                    "3": "parallel trees",
                }
                sorted_keys = [mode_to_name[mode] for mode in sorted_keys]

            avg_data_points = sum([x[1] for x in grouped_data.values()]) / len(grouped_data.values())
            # Plot grouped data
            if (len(filter_list) == 1):
                axis = axes
            else:
                axis = axes[fig_num // num_cols, fig_num % num_cols] # type: plt.Axes
            axis.plot(sorted_keys, sorted_data)
            # if error_bars:
            #     # axis.errorbar(sorted_keys, sorted_data, yerr=[], fmt='o', capsize=5, capthick=2)
            #     axis.errorbar(sorted_keys, sorted_data, yerr=error_data, fmt='o', capsize=5, capthick=2, label=str(filter))
            # else:
            axis.scatter(sorted_keys, sorted_data, label=str(filter))
            axis.legend()
            axis.set_xlabel(x_axis)
            axis.set_ylabel(y_axis)
            axis.set_title(y_axis + " vs " + x_axis)
            for x,y in grouped_data.items():
                axis.annotate(f"{y[1]}", (x,y[0]))
            if y_axis == "win":
                axis.set_ylim((0, 1))
    # delete unused subplots
    for fig_num in range(len(filter_list), num_rows * num_cols):
        if (len(filter_list) == 1):
            axis = axes
        else:
            axis = axes[fig_num // num_cols, fig_num % num_cols]
        fig.delaxes(axis)
    # plt.tight_layout()
    # if y_axis == "win":
    #     plt.ylim((0, 1))
    plt.show()
    

if __name__ == "__main__":
    """
    level
    threads
    time_ms
    ucb_const
    rollout_mode
    win
    num_steps
    """
    """
    optimal ucb_const:
    mode normal: 0.2
    mode max_node: 0.2
    mode 2: ~0.2
    mode 3: 0.2
    """
    # filter_criteria = {"level": 9, "threads": 4}
    target_level = "9+"
    r_mode = MAX_NODE
    ucb = 0.01
    rollout_mode = mcts.NORMAL_MCTS
    filters = [
        # [
        #     {"level": target_level, "rollout_mode": NORMAL_MCTS, "heuristic_mode": 0, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": MAX_NODE, "heuristic_mode": 0, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": AVG_NODE, "heuristic_mode": 0, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": PARALLEL_TREES, "heuristic_mode": 0, "ucb_const": ucb},
        # ],
        # [
        #     {"level": target_level, "rollout_mode": NORMAL_MCTS, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": MAX_NODE, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": AVG_NODE, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": PARALLEL_TREES, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": ucb},
        # ]
        # ==============================================================================================================
        # Compare UCB values for r_mode rollout mode using different heuristic modes
        # ==============================================================================================================
        # [
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": NO_HEURISTIC, "ucb_const": 0.01},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": NO_HEURISTIC, "ucb_const": 0.1},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": NO_HEURISTIC, "ucb_const": 0.2},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": NO_HEURISTIC, "ucb_const": 0.5},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": NO_HEURISTIC, "ucb_const": 1.0},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": NO_HEURISTIC, "ucb_const": 1.4},
        # ],
        # [
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_MCTS, "ucb_const": 0.01},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_MCTS, "ucb_const": 0.1},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_MCTS, "ucb_const": 0.2},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_MCTS, "ucb_const": 0.5},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_MCTS, "ucb_const": 1.0},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_MCTS, "ucb_const": 1.4},
        # ],
        # [
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": 0.01},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": 0.1},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": 0.2},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": 0.5},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": 1.0},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_SELECT, "ucb_const": 1.4},
        # ],
        # [
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_EXPAND, "ucb_const": 0.01},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_EXPAND, "ucb_const": 0.1},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_EXPAND, "ucb_const": 0.2},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_EXPAND, "ucb_const": 0.5},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_EXPAND, "ucb_const": 1.0},
        #     {"level": target_level, "rollout_mode": r_mode, "heuristic_mode": HEURISTIC_EXPAND, "ucb_const": 1.4},
        # ],
        # ==============================================================================================================
        # Compare rollouts with different heuristic modes using a single ucb constant
        # ==============================================================================================================
        # [
        #     {"level": target_level, "rollout_mode": NORMAL_MCTS, "heuristic_mode": 0, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": NORMAL_MCTS, "heuristic_mode": 1, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": NORMAL_MCTS, "heuristic_mode": 2, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": NORMAL_MCTS, "heuristic_mode": 3, "ucb_const": ucb},
        # ],
        # [
        #     {"level": target_level, "rollout_mode": MAX_NODE, "heuristic_mode": 0, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": MAX_NODE, "heuristic_mode": 1, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": MAX_NODE, "heuristic_mode": 2, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": MAX_NODE, "heuristic_mode": 3, "ucb_const": ucb},
        # ],
        # [
        #     {"level": target_level, "rollout_mode": AVG_NODE, "heuristic_mode": 0, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": AVG_NODE, "heuristic_mode": 1, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": AVG_NODE, "heuristic_mode": 2, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": AVG_NODE, "heuristic_mode": 3, "ucb_const": ucb},
        # ],
        # [
        #     {"level": target_level, "rollout_mode": PARALLEL_TREES, "heuristic_mode": 0, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": PARALLEL_TREES, "heuristic_mode": 1, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": PARALLEL_TREES, "heuristic_mode": 2, "ucb_const": ucb},
        #     {"level": target_level, "rollout_mode": PARALLEL_TREES, "heuristic_mode": 3, "ucb_const": ucb},
        # ],
        # ==============================================================================================================
        # Comparing selection modes
        # ==============================================================================================================
        [
            {"level": target_level, "rollout_mode": rollout_mode, "heuristic_mode": mcts.HEURISTIC_SELECT, "ucb_const": 0.01, "selection_mode": mcts.FULL_EXPAND},
            {"level": target_level, "rollout_mode": rollout_mode, "heuristic_mode": mcts.HEURISTIC_SELECT, "ucb_const": 0.01, "selection_mode": mcts.SQUARE_RATIO},
        ],
        [
            {"level": target_level, "rollout_mode": rollout_mode, "heuristic_mode": mcts.HEURISTIC_SELECT, "ucb_const": 0.2, "selection_mode": mcts.FULL_EXPAND},
            {"level": target_level, "rollout_mode": rollout_mode, "heuristic_mode": mcts.HEURISTIC_SELECT, "ucb_const": 0.2, "selection_mode": mcts.SQUARE_RATIO},
        ],
        [
            {"level": target_level, "rollout_mode": rollout_mode, "heuristic_mode": mcts.HEURISTIC_SELECT, "ucb_const": 1.4, "selection_mode": mcts.FULL_EXPAND},
            {"level": target_level, "rollout_mode": rollout_mode, "heuristic_mode": mcts.HEURISTIC_SELECT, "ucb_const": 1.4, "selection_mode": mcts.SQUARE_RATIO},
        ]
        # ==============================================================================================================
        # [
        #     {"level": target_level, "rollout_mode": mcts.PARALLEL_TREES, "heuristic_mode": 0, "ucb_const": 0.2},
        #     # {"level": target_level, "rollout_mode": mcts.PARALLEL_TREES, "heuristic_mode": 1, "ucb_const": 0.2},
        #     {"level": target_level, "rollout_mode": mcts.PARALLEL_TREES, "heuristic_mode": 2, "ucb_const": 0.2},
        #     # {"level": target_level, "rollout_mode": mcts.PARALLEL_TREES, "heuristic_mode": 3, "ucb_const": 0.2},
        # ],
        # [
        #     {"level": "9", "rollout_mode": 1, "heuristic_mode": 0, "time_ms": "200"},
        #     {"level": "9", "rollout_mode": 1, "heuristic_mode": 1, "time_ms": "200"},
        #     {"level": "9", "rollout_mode": 1, "heuristic_mode": 2, "time_ms": "200"},
        #     {"level": "9", "rollout_mode": 1, "heuristic_mode": 3, "time_ms": "200"},
        # ]
    ]
    x_axis = "time_ms"
    y_axis = "win"

    test_generate_plot(CSV_FILENAME, x_axis, y_axis, filters, log=False, graph=True)#, filter_2, filter_3])
    exit()
    # generate_plot(CSV_FILENAME, filter_criteria, x_axis, y_axis)
    # play_level1()
    # print()
    # play_level2()
    # print()
    # play_level3()
    # print()
    # play_level4()
    play_level1()
    print()
    play_level2()
    print()
    play_level3()
    print()
    play_level4()
    print()
    play_level9()
    print()
    # level = level.Level(5, 10, 10, level_data_1, chosen_plants_1)
    # print(level.rollout(8, 10000, 1))
    # print(level.rollout(8, 10000, 2))
    # print(level.rollout(8, 10000, 3))
    # print(level.timed_rollout(8, 2000, 1))
    # print(level.timed_rollout(8, 2000, 2))
    # print(level.timed_rollout(8, 2000, 3))

    # animate_observation(level)
    # run_animation()
    # estimate_simulation_speed()
    # import pstats
    # p = pstats.Stats('profile.txt')
    # p.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    # cProfile.run('run_animation()')
    # while not level.done:
    #     level.step(level.get_random_action())
    #     obs = get_numpy_arr_from_level_obs(level)
    #     pprobs)