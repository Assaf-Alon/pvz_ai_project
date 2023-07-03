from build import level
from build import mcts
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import make_interp_spline, CubicSpline, BSpline
from pprint import pprint
import cProfile
from time import time
import json
import csv


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
    env = level.Level(1, 10, FPS, get_level_info(1))
    print(f"Level 1 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 1 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 1 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level2():
    FPS = 10
    GAMES = 10000
    env = level.Level(3, 10, FPS, get_level_info(2))
    print(f"Level 2 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 2 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 2 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level3():
    FPS = 10
    GAMES = 10000
    env = level.Level(3, 10, FPS, get_level_info(3))
    print(f"Level 3 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 3 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 3 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level4():
    FPS = 10
    GAMES = 100000
    env = level.Level(5, 10, FPS, get_level_info(4))
    print(f"Level 4 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 4 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 4 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def csv_append(new_data: dict, filename=CSV_FILENAME):
    """
    CSV columns are:
    level, time_ms, threads, ucb_const, rollout_mode, win, num_steps
    NOTE: num_steps is the number of steps needed to achieve a state from which empty steps give a victory!!! set to -1 for losses.
    """
    data_csv = open(filename, "a+")
    data_writer = csv.writer(data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
    new_row = [new_data["level"], new_data["time_ms"], new_data["threads"], new_data["ucb_const"], new_data["rollout_mode"], new_data["win"], new_data["num_steps"]]
    data_writer.writerow(new_row)

import pandas as pd
import matplotlib.pyplot as plt


import pandas as pd
import matplotlib.pyplot as plt

def test_generate_plot(csv_file, x_axis, y_axis, filters, log, graph):
    # Read the data from CSV
    data = pd.read_csv(csv_file)
    avg_func = lambda series: sum(series) / len(series)
    plt.figure(figsize=(8,8))
    # Generate graphs for each filter
    filter_info = ""
    for idx, filter in enumerate(filters):
        # Apply the filter
        filtered_data = data.copy()
        for key, value in filter.items():
            filtered_data = filtered_data[filtered_data[key] == value]

        # Group the filtered data by x-axis values and calculate the mean of y-axis values
        # grouped_data = filtered_data.groupby(x_axis)[y_axis].mean().reset_index()
        grouped_data = filtered_data.groupby(x_axis)[y_axis].agg(avg_func).reset_index()
        data_counts = data[x_axis].value_counts().reset_index()
        # data_counts.columns = [x_axis, 'samples']

        # merged_data = pd.merge(grouped_data, data_counts, on=x_axis)

        mean_sample_num = filtered_data.groupby(x_axis)[y_axis].count().mean()

        # Plot the graph
        plt.scatter(grouped_data[x_axis], grouped_data[y_axis], label=f'Filter {idx + 1}')
        if graph:
            plt.plot(grouped_data[x_axis], grouped_data[y_axis], label=f'Filter {idx + 1}')
        
        for x, y, count in zip(grouped_data[x_axis], grouped_data[y_axis], data_counts):
            plt.annotate(f'samples: {count}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
        x = grouped_data[x_axis]
        y = grouped_data[y_axis]
        # spline = CubicSpline(x, y)
        # spline = make_interp_spline(x, y, k=3)  # type: "BSpline"
        # x_new = np.linspace(x.min(), x.max(), 300)
        # smooth_curve = spline(x_new)
        # window_size = 10  # Adjust the window size as needed
        # smooth_curve = np.convolve(smooth_curve, np.ones(window_size) / window_size, mode='same')
        
        # Plot the smooth curve
        # plt.plot(x_new, smooth_curve)

        annotation_y_pos = 1 - idx * 0.04  # Adjust vertical position based on filter index
        annotation_y_pos = 1.05 - (idx * 0.1 / len(filters))  # Adjust vertical position based on filter index and number of filters
        filter_text = ', '.join([f'{key}: {value}' for key, value in filter.items()])
        filter_text = f"{filter_text} (Mean samples: {mean_sample_num:.2f})"
        filter_info = f"{filter_info}Filter {idx + 1}: {filter_text}\n"
        # plt.annotate(f'Filter {idx+1}: {filter_text}', xy=(0.5, annotation_y_pos), xycoords='axes fraction', xytext=(0, 10),
        #              textcoords='offset points', ha='center', va='bottom')

    # Display the graph
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    # plt.figtext(0.5, 0.05, filter_info, ha="center", fontsize=8)
    # plt.text(0.5, -0.3, 'Additional Text Below X-axis Label', ha='center', va='top', transform=plt.gca().transAxes)
    # plt.title(f"Plot of {y_axis} against {x_axis}" + "\n" + filter_info)
    plt.title(filter_info)
    if log:
        plt.xscale('log')
    # plt.text(0.5, -0.2, f'Filter Information:\n{filter_info}', ha='center', va='top', transform=plt.gca().transAxes)
    plt.legend()
    plt.show()


def generate_plot(csv_file, filter_criteria, x_axis, y_axis, comparison_dict=None):
    data = pd.read_csv(csv_file)
    for key, value in filter_criteria.items():
        data = data.loc[data[key] == value]
    
    if comparison_dict is not None:
        for key, value in comparison_dict.items():
            data1 = data.loc[data[comparison_dict[key]] == value]
    grouped_data = data.groupby(x_axis)[y_axis].mean().reset_index()

    data_counts = data[x_axis].value_counts().reset_index()
    data_counts.columns = [x_axis, 'samples']

    merged_data = pd.merge(grouped_data, data_counts, on=x_axis)
    

    plt.scatter(merged_data[x_axis], merged_data[y_axis])

    for x, y, count in zip(merged_data[x_axis], merged_data[y_axis], merged_data['samples']):
        plt.annotate(f'samples: {count}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

    filter_text = ', '.join([f'{key}: {value}' for key, value in filter_criteria.items()])
    plt.annotate(f'Filter: {filter_text}', xy=(0.5, 1), xycoords='axes fraction', xytext=(0, 10),
                 textcoords='offset points', ha='center', va='bottom')

    plt.show()
    # # Read the CSV file into a pandas DataFrame
    # df = pd.read_csv(csv_file)
    
    # # Filter the data based on the given criteria
    # for key, value in filter_criteria.items():
    #     df = df.loc[df[key] == value]
    
    # # for data points for the same x value, take the mean of the y values
    # df = df.groupby(x_axis).mean().reset_index()

    # # Generate the plot
    # plt.scatter(df[x_axis], df[y_axis])
    # plt.xlabel(x_axis)
    # plt.ylabel(y_axis)
    # plt.title(f"Plot of {y_axis} against {x_axis}")
    # plt.show()



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
    optimal threads:
    mode 0: lmao
    mode 1: 4
    mode 2: 8
    mode 3: 8
    """
    # filter_criteria = {"level": 9, "threads": 4}
    filters = [
        {"level": 9, "threads": 8, "rollout_mode": 1},
        {"level": 9, "threads": 8, "rollout_mode": 2},
        {"level": 9, "threads": 8, "rollout_mode": 3}
    ]
    x_axis = "ucb_const"
    y_axis = "win"

    test_generate_plot(CSV_FILENAME, x_axis, y_axis, filters, log=True, graph=True)#, filter_2, filter_3])
    # generate_plot(CSV_FILENAME, filter_criteria, x_axis, y_axis)
    # play_level1()
    # print()
    # play_level2()
    # print()
    # play_level3()
    # print()
    # play_level4()
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