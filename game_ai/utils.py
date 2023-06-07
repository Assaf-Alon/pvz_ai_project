import cpp_env.level as cpp_level
import numpy as np
from matplotlib import pyplot as plt
from pprint import pprint

level_data_1 = cpp_level.ZombieQueue()
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(11, 1, "normal"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(12, 1, "normal"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(20, 3, "normal"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(20, 2, "buckethead"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "flag"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(50, 4, "newspaper"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "conehead"))
level_data_1.push_back(cpp_level.ZombieSpawnTemplate(85, 1, "normal"))


level_data_2 = cpp_level.ZombieQueue()
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(11, 1, "normal"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(12, 1, "normal"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(20, 3, "normal"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(20, 2, "buckethead"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "flag"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(50, 4, "newspaper"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(50, 1, "conehead"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(85, 1, "normal"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(85, 2, "normal"))
level_data_2.push_back(cpp_level.ZombieSpawnTemplate(85, 3, "normal"))

chosen_plants_1 = [int(cpp_level.SUNFLOWER), int(cpp_level.PEASHOOTER), int(cpp_level.POTATOMINE), int(cpp_level.SQUASH), int(cpp_level.SPIKEWEED), int(cpp_level.WALLNUT)]
chosen_plants_basic = [cpp_level.SUNFLOWER, cpp_level.PEASHOOTER]

def construct_level_data_from_list(list: list):
    list.sort(lambda item: item[0])
    level_data = cpp_level.ZombieQueue()
    for item in list:
        level_data.push_back(cpp_level.ZombieSpawnTemplate(item[0], item[1], item[2]))
    return level_data

def get_numpy_arr_from_level_obs(level: cpp_level.Level):
    arr = level.get_observation()
    result = np.zeros((level.lanes, level.cols, 3))
    for i in range(level.lanes):
        for j in range(level.cols):
            obs = arr[i][j] # type: cpp_level.CellObservation
            result[i,j,0] = obs.plant_type
            result[i,j,1] = obs.plant_hp_phase
            result[i,j,2] = obs.zombie_danger_level
    return result

def print_level_state(level: cpp_level.Level):
    state = level.get_state() # type: cpp_level.State
    for lane in range(state.size()):
        for col in range(state[lane].size()):
            cell = state[lane][col] # type: cpp_level.Cell

if __name__ == "__main__":
    level = cpp_level.Level(5, 10, 10, level_data_1, chosen_plants_basic)
    while not level.done:
        level.step(level.get_random_action())
        obs = get_numpy_arr_from_level_obs(level)
        pprint(obs)