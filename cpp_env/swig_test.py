import level
import time
import copy
from enum import Enum

class PlantName(Enum):
    NO_PLANT = 0
    CHERRYBOMB = 1
    CHOMPER = 2
    HYPNOSHROOM = 3
    ICESHROOM = 4
    JALAPENO = 5
    PEASHOOTER = 6
    POTATOMINE = 7
    PUFFSHROOM = 8
    REPEATERPEA = 9
    SCAREDYSHROOM = 10
    SNOWPEA = 11
    SPIKEWEED = 12
    SQUASH = 13
    SUNFLOWER = 14
    SUNSHROOM = 15
    THREEPEATER = 16
    WALLNUT = 17
    NUM_PLANTS = 18

"""
level_data.push_back(ZombieSpawnTemplate{.second = 10, .lane = 1, .type = "normal"});
level_data.push_back(ZombieSpawnTemplate{.second = 11, .lane = 1, .type = "normal"});
level_data.push_back(ZombieSpawnTemplate{.second = 12, .lane = 1, .type = "normal"});
level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 3, .type = "normal"});
level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 2, .type = "buckethead"});
level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 1, .type = "flag"});
level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 4, .type = "newspaper"});
level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 1, .type = "conehead"});
level_data.push_back(ZombieSpawnTemplate{.second = 85, .lane = 1, .type = "normal"});
"""
# tmp = LegalPlantVector()
tmp = level.LegalPlantVector()
chosen_plants = [int(level.SUNFLOWER), int(level.PEASHOOTER), int(level.POTATOMINE), int(level.SQUASH), int(level.SPIKEWEED), int(level.WALLNUT)]
for i in range(len(chosen_plants)):
    tmp.push_back(chosen_plants[i])

tmp2 = level.ZombieQueue()
tmp2.push_back(level.ZombieSpawnTemplate(10, 1, "normal"))
tmp2.push_back(level.ZombieSpawnTemplate(11, 1, "normal"))
tmp2.push_back(level.ZombieSpawnTemplate(12, 1, "normal"))
tmp2.push_back(level.ZombieSpawnTemplate(20, 3, "normal"))
tmp2.push_back(level.ZombieSpawnTemplate(20, 2, "buckethead"))
tmp2.push_back(level.ZombieSpawnTemplate(50, 1, "flag"))
tmp2.push_back(level.ZombieSpawnTemplate(50, 4, "newspaper"))
tmp2.push_back(level.ZombieSpawnTemplate(50, 1, "conehead"))
tmp2.push_back(level.ZombieSpawnTemplate(85, 1, "normal"))
start = time.time()
env = level.Level(5, 10, 10, tmp2, chosen_plants)
print(env.frame)
env2 = copy.copy(env)
env.step(0, 1, 1)
env.step(0, 1, 1)
env.step(0, 1, 1)
print(env.frame)
print(env2.frame)
# wins = env.rollout(8, 100000)
end = time.time()
# print(wins)
print(f"time taken: {end - start} ") #, time per game: {(end - start) / 100000}")
