import level
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pprint import pprint
import cProfile
from time import time
import json


def construct_level_data_from_list(list: list):
    list.sort(key=lambda item: item[0]) # sort by first element of tuple (list[tuple])
    level_data = level.ZombieQueue()
    for item in list:
        level_data.push_back(level.ZombieSpawnTemplate(item[0], item[1], item[2]))
    return level_data



# level_data_1_list = [
#     (10, 1, "normal"),
#     (11, 1, "normal"),
#     (12, 1, "normal"),
#     (20, 3, "normal"),
#     (20, 2, "buckethead"),
#     (50, 1, "flag"),
#     (50, 4, "newspaper"),
#     (50, 1, "conehead"),
#     (85, 1, "normal")
# ]
# level_data_1 = construct_level_data_from_list(level_data_1_list)

# level_data_2_list = [
#     (10, 1, "normal"), 
#     (11, 1, "normal"), 
#     (12, 1, "normal"), 
#     (20, 3, "normal"), 
#     (20, 2, "buckethead"), 
#     (50, 1, "flag"), 
#     (50, 4, "newspaper"), 
#     (50, 1, "conehead"), 
#     (85, 1, "normal"), 
#     (85, 2, "normal"), 
#     (85, 3, "normal")
# ]

chosen_plants_1 = [level.SUNFLOWER, level.PEASHOOTER, level.POTATOMINE, level.SQUASH, level.SPIKEWEED, level.WALLNUT]
chosen_plants_basic = [level.SUNFLOWER, level.PEASHOOTER]
lvl9_legal_plants = [level.SUNFLOWER, level.PEASHOOTER, level.WALLNUT, level.POTATOMINE, level.REPEATERPEA, level.CHERRYBOMB]
# Actual levels
with open("data/levels.json", "r") as level_json:
    levels = json.load(level_json)
lvl1_data = construct_level_data_from_list(levels["level_1"])
lvl2_data = construct_level_data_from_list(levels["level_2"])
lvl3_data = construct_level_data_from_list(levels["level_3"])
lvl4_data = construct_level_data_from_list(levels["level_4"])
lvl9_data = construct_level_data_from_list(levels["level_9"])

chosen_plants_lvl1 = [level.PEASHOOTER]
chosen_plants_lvl2 = [level.PEASHOOTER, level.SUNFLOWER]
chosen_plants_lvl3 = [level.PEASHOOTER, level.SUNFLOWER, level.CHERRYBOMB]
chosen_plants_lvl4 = [level.PEASHOOTER, level.SUNFLOWER, level.CHERRYBOMB, level.WALLNUT]



def get_numpy_arr_from_level_obs(level: level.Level):
    arr = level.get_observation()
    result = np.asarray(arr)
    return result

def print_level_state(level: level.Level):
    state = level.get_state() # type: level.State
    for lane in range(state.size()):
        for col in range(state[lane].size()):
            cell = state[lane][col] # type: level.Cell

def get_frame_from_obs(observation: np.ndarray):
    num_rows, num_cols, _ = observation.shape

    # Create a blank frame
    frame = np.zeros((num_rows, num_cols * 2, 3))

    # Iterate over each cell in the observation
    for row in range(num_rows):
        for col in range(num_cols):
            plant_type, hp_thirds, zombie_danger = observation[row][col]

            # Calculate the color for the left half of the cell based on plant_type and hp_thirds
            if plant_type == 0:
                left_color = [0, 0, 0]  # Black
            else:
                if hp_thirds == 1:
                    left_color = [1, 0, 0]  # Red
                elif hp_thirds == 2:
                    left_color = [1, 1, 0]  # Yellow
                elif hp_thirds == 3:
                    left_color = [0, 1, 0]  # Green
                else:
                    left_color = [0, 0, 0]  # Black

            # Calculate the color for the right half of the cell based on zombie_danger
            right_color_intensity = min(1.0, zombie_danger / 5.0)
            right_color = [right_color_intensity, 0, 0]  # Shades of red based on zombie_danger

            # Set the colors for the left and right halves of the cell in the frame
            frame[row][col * 2] = left_color
            frame[row][col * 2 + 1] = right_color

    return frame

def animate_observation_buffer(frame_buffer: list):
    fig, ax = plt.subplots()
    # Set up an initial plot with the first frame
    im = ax.imshow(frame_buffer[0])

    # Define the update function for the animation
    def update(frame):
        # print(frame)
        # Update the plot with the next frame
        im.set_array(frame_buffer[frame])
        return [im]

    # Create the animation object using the FuncAnimation class
    anim = animation.FuncAnimation(fig, update, frames=len(frame_buffer), interval=1, blit=True)
    num_cols = frame_buffer[0].shape[1] // 2
    num_rows = frame_buffer[0].shape[0]
    aspect_ratio = num_cols / frame_buffer[0].shape[0]

    # Set custom tick positions for half-width columns
    ax.set_xticks(np.arange(num_cols) * 2 + 0.5)
    ax.set_yticks(np.arange(frame_buffer[0].shape[0]) + 0.5)
    ax.set_xticklabels(list(range(num_cols)))
    ax.set_yticklabels(list(range(num_rows)))
    # Show the animation
    plt.show()

def run_animation():
    level = level.Level(5, 10, 10, lvl1_data, chosen_plants_basic)
    frame_list = []
    while not level.done:
        level.step(level.get_random_action())
        obs = get_numpy_arr_from_level_obs(level)
        frame = get_frame_from_obs(obs)
        frame_list.append(frame)
    animate_observation_buffer(frame_list)

def simulate_set_game(level: level.Level, action_list: list[level.Action]):
    frames = []
    for action in action_list:
        while not level.is_action_legal(action) and not level.done:
            level.step()
            frames.append(get_frame_from_obs(get_numpy_arr_from_level_obs(level)))
        level.step(action)
        frames.append(get_frame_from_obs(get_numpy_arr_from_level_obs(level)))
    while not level.done:
        level.step()
        frames.append(get_frame_from_obs(get_numpy_arr_from_level_obs(level)))
    # print(f"lawnmowers: {level.lawnmowers[0]} {level.lawnmowers[1]} {level.lawnmowers[2]} {level.lawnmowers[3]} {level.lawnmowers[4]}")
    animate_observation_buffer(frames)

plant_to_name = ("no_plant","cherrybomb","chomper","hypnoshroom","iceshroom","jalapeno","peashooter","potatomine","puffshroom","repeaterpea","scaredyshroom","snowpea","spikeweed","squash","sunflower","sunshroom","threepeater","wallnut")

def action_to_string(action: level.Action):
    return f"action: plant {plant_to_name[action.plant_name]} at coords: {action.lane}, {action.col}"
    
def estimate_simulation_speed():
    level = level.Level(5, 10, 10, lvl1_data, chosen_plants_basic)
    num_rollout = 1000000
    start = time()
    level.rollout(14, num_rollout)
    end = time()
    print(f"total time: {end-start}, time per rollout: {(end-start)/num_rollout}")

def play_level1():
    FPS = 10
    GAMES = 10000
    env = level.Level(1, 10, FPS, lvl1_data, chosen_plants_lvl1)
    print(f"Level 1 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 1 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 1 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level2():
    FPS = 10
    GAMES = 10000
    env = level.Level(3, 10, FPS, lvl2_data, chosen_plants_lvl2)
    print(f"Level 2 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 2 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 2 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level3():
    FPS = 10
    GAMES = 10000
    env = level.Level(3, 10, FPS, lvl3_data, chosen_plants_lvl3)
    print(f"Level 3 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 3 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 3 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

def play_level4():
    FPS = 10
    GAMES = 100000
    env = level.Level(5, 10, FPS, lvl4_data, chosen_plants_lvl4)
    print(f"Level 4 Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
    print(f"Level 4 Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
    print(f"Level 4 Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")

if __name__ == "__main__":
    play_level1()
    print()
    play_level2()
    print()
    play_level3()
    print()
    play_level4()
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