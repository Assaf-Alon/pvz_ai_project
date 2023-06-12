import cpp_env.level as cpp_level
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pprint import pprint
import cProfile
from time import time


def construct_level_data_from_list(list: list):
    list.sort(key=lambda item: item[0]) # sort by first element of tuple (list[tuple])
    level_data = cpp_level.ZombieQueue()
    for item in list:
        level_data.push_back(cpp_level.ZombieSpawnTemplate(item[0], item[1], item[2]))
    return level_data


# level_data_1 = cpp_level.ZombieQueue()
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(11, 1, "normal"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(12, 1, "normal"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(20, 3, "normal"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(20, 2, "buckethead"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "flag"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(50, 4, "newspaper"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "conehead"))
# level_data_1.push_back(cpp_level.ZombieSpawnTemplate(85, 1, "normal"))

level_data_1_list = [
    (10, 1, "normal"),
    (11, 1, "normal"),
    (12, 1, "normal"),
    (20, 3, "normal"),
    (20, 2, "buckethead"),
    (50, 1, "flag"),
    (50, 4, "newspaper"),
    (50, 1, "conehead"),
    (85, 1, "normal")
]
level_data_1 = construct_level_data_from_list(level_data_1_list)

# level_data_2 = cpp_level.ZombieQueue()
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(11, 1, "normal"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(12, 1, "normal"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(20, 3, "normal"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(20, 2, "buckethead"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "flag"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(50, 4, "newspaper"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "conehead"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(85, 1, "normal"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(85, 2, "normal"))
# level_data_2.push_back(cpp_level.ZombieSpawnTemplate(85, 3, "normal"))

level_data_2_list = [
    (10, 1, "normal"), 
    (11, 1, "normal"), 
    (12, 1, "normal"), 
    (20, 3, "normal"), 
    (20, 2, "buckethead"), 
    (50, 1, "flag"), 
    (50, 4, "newspaper"), 
    (50, 1, "conehead"), 
    (85, 1, "normal"), 
    (85, 2, "normal"), 
    (85, 3, "normal")
]
level_data_2 = construct_level_data_from_list(level_data_2_list)

chosen_plants_1 = [cpp_level.SUNFLOWER, cpp_level.PEASHOOTER, cpp_level.POTATOMINE, cpp_level.SQUASH, cpp_level.SPIKEWEED, cpp_level.WALLNUT]
chosen_plants_basic = [cpp_level.SUNFLOWER, cpp_level.PEASHOOTER]



def get_numpy_arr_from_level_obs(level: cpp_level.Level):
    arr = level.get_observation()
    result = np.asarray(arr)
    return result

def print_level_state(level: cpp_level.Level):
    state = level.get_state() # type: cpp_level.State
    for lane in range(state.size()):
        for col in range(state[lane].size()):
            cell = state[lane][col] # type: cpp_level.Cell

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
        print(frame)
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
    level = cpp_level.Level(5, 10, 10, level_data_1, chosen_plants_basic)
    frame_list = []
    while not level.done:
        level.step(level.get_random_action())
        obs = get_numpy_arr_from_level_obs(level)
        frame = get_frame_from_obs(obs)
        frame_list.append(frame)
    animate_observation_buffer(frame_list)

def estimate_simulation_speed():
    level = cpp_level.Level(5, 10, 10, level_data_1, chosen_plants_basic)
    num_rollout = 1000000
    start = time()
    level.rollout(14, num_rollout)
    end = time()
    print(f"total time: {end-start}, time per rollout: {(end-start)/num_rollout}")


if __name__ == "__main__":
    # level = cpp_level.Level(5, 10, 10, level_data_1, chosen_plants_1)
    # print(level.rollout(8, 10000, 1))
    # print(level.rollout(8, 10000, 2))
    # print(level.rollout(8, 10000, 3))

    # animate_observation(level)
    run_animation()
    # estimate_simulation_speed()
    # import pstats
    # p = pstats.Stats('profile.txt')
    # p.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    # cProfile.run('run_animation()')
    # while not level.done:
    #     level.step(level.get_random_action())
    #     obs = get_numpy_arr_from_level_obs(level)
    #     pprobs)