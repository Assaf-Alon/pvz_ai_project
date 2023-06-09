import cpp_env.level as cpp_level
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pprint import pprint
import cProfile


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

def animate_observation(level: cpp_level.Level):
    color_mapping = {
        1: 'red',
        2: 'yellow',
        3: 'green'
    }

    # Define the colors for the right half of the cell based on the third number
    def get_right_half_color(value):
        if value == 0:
            return 'black'
        else:
            intensity = min(1.0, value / 10.0)  # Normalize the value to range between 0 and 1
            return (intensity, 0, 0)  # Shades of red based on the intensity

    # Create a figure and axis object for the animation
    fig, ax = plt.subplots()

    # Define the update function
    def update(frame):
        level.step(level.get_random_action())
        print(frame)
        board = get_numpy_arr_from_level_obs(level)

        # Clear the axis
        ax.clear()

        # Get the dimensions of the board
        num_rows, num_cols, _ = board.shape

        # Iterate over each cell in the board
        for row in range(num_rows):
            for col in range(num_cols):
                # Get the values from the current cell
                plant_type, hp_thirds, zombie_danger = board[row][col]
                # Calculate the coordinates of the current cell in the plot
                x = col
                y = num_rows - row - 1  # Invert the y-axis to match the numpy array indexing

                # Determine the color for the left half of the cell
                if plant_type == 0:
                    left_color = 'black'
                else:
                    left_color = color_mapping.get(hp_thirds)

                # Determine the color for the right half of the cell
                right_color = get_right_half_color(zombie_danger)

                # Plot the left half of the cell
                ax.fill([x, x, x + 0.5, x + 0.5], [y, y + 1, y + 1, y], color=left_color)

                # Plot the right half of the cell
                ax.fill([x + 0.5, x + 0.5, x + 1, x + 1], [y, y + 1, y + 1, y], color=right_color)

        # Set plot configurations
        ax.set_xlim([0, num_cols])
        ax.set_ylim([0, num_rows])
        ax.set_aspect('equal')  # Set equal aspect ratio for square cells

        # Return the modified axis
        return ax

    # Create the animation object using the FuncAnimation class
    anim = animation.FuncAnimation(fig, update, frames=1000, interval=0, blit=False)

    # Show the animation
    plt.show()

def run_animation():
    level = cpp_level.Level(5, 10, 10, level_data_1, chosen_plants_basic)
    animate_observation(level)

if __name__ == "__main__":
    # level = cpp_level.Level(5, 10, 10, level_data_1, chosen_plants_basic)
    # animate_observation(level)
    import pstats
    p = pstats.Stats('profile.txt')
    p.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    # cProfile.run('run_animation()')
    # while not level.done:
    #     level.step(level.get_random_action())
    #     obs = get_numpy_arr_from_level_obs(level)
    #     pprobs)