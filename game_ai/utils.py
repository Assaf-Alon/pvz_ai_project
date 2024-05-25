from build import level
from build import mcts
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time
import json
import csv
import matplotlib.animation as animation


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

def animate_observation_buffer(observation_buffer: list, output_path='animation.mp4'):
    fig, ax = plt.subplots(figsize=(10, 10))
    annotations = []

    im = ax.imshow(get_frame_from_observation(observation_buffer[0]))

    def update(frame):
        im.set_array(get_frame_from_observation(observation_buffer[frame]))
        for annotation in annotations:
            annotation.remove()
        annotations.clear()
        for plant_name, row, col in get_plants_from_observation(observation_buffer[frame]):
            annotations.append(ax.annotate(plant_name, xy=(col * 2 + 0.5, row), xycoords="data", ha="center", va="center", wrap=True, bbox=dict(boxstyle="round", fc="w")))
        return im, *annotations

    num_cols = observation_buffer[0].shape[1] // 2
    num_rows = observation_buffer[0].shape[0]
    ax.set_aspect(2)

    ax.set_xticks(np.arange(num_cols) * 2 + 0.5)
    ax.set_yticks(np.arange(observation_buffer[0].shape[0]) + 0.5)
    ax.set_xticklabels(list(range(num_cols)))
    ax.set_yticklabels(list(range(num_rows)))

    anim = animation.FuncAnimation(fig, update, frames=len(observation_buffer), interval=5, blit=True)

    # Save the animation as an MP4 file
    anim.save(output_path, writer='ffmpeg', fps=60)

    plt.close(fig)

def run_animation():
    level1 = level.Level(5, 10, 10, *get_level_info(1))
    frame_list = []
    while not level1.done:
        level1.step(level1.get_random_action())
        obs = get_numpy_arr_from_level_obs(level1)
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
    animate_observation_buffer(observations)

# Initialize the figure and axis once
obs_fig, obs_ax = plt.subplots(figsize=(10, 10))
annotations = []
obs_im = None

def draw_observation(observation, frame_num):
    global annotations
    global obs_im
    observation = np.asarray(observation)
    if obs_im is None:
        # Initialize the image data
        obs_im = obs_ax.imshow(get_frame_from_observation(observation))
    # Update the image data
    obs_im.set_data(get_frame_from_observation(observation))

    # Remove existing annotations
    for annotation in annotations:
        annotation.remove()
    annotations.clear()

    # Add new annotations
    for plant_name, row, col in get_plants_from_observation(observation):
        annotations.append(obs_ax.annotate(plant_name, xy=(col * 2 + 0.5, row), xycoords="data", ha="center", va="center", wrap=True, bbox=dict(boxstyle="round", fc="w")))

    num_cols = observation.shape[1] // 2
    num_rows = observation.shape[0]
    obs_ax.set_aspect(2)

    obs_ax.set_xticks(np.arange(num_cols) * 2 + 0.5)
    obs_ax.set_yticks(np.arange(observation.shape[0]) + 0.5)
    obs_ax.set_xticklabels(list(range(num_cols)))
    obs_ax.set_yticklabels(list(range(num_rows)))
    plt.title(f"Frame {frame_num}")

    plt.draw()
    plt.pause(0.0001)  # Adjust the pause interval as needed

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
    new_row = [new_data["level"], new_data["time_ms"], new_data["parallel_factor"], new_data["ucb_const"], new_data["rollout_mode"], new_data["heuristic_mode"], new_data["selection_mode"], new_data["loss_heuristic"], new_data["win"], new_data["num_steps"]]
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
