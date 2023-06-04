import level
import time

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
env = level.Level(5, 10, 10, chosen_plants)
env.append_zombie(10, 1, "normal")
env.append_zombie(11, 1, "normal")
env.append_zombie(12, 1, "normal")
env.append_zombie(20, 3, "normal")
env.append_zombie(20, 2, "buckethead")
env.append_zombie(50, 1, "flag")
env.append_zombie(50, 4, "newspaper")
env.append_zombie(50, 1, "conehead")
env.append_zombie(85, 1, "normal")
start = time.time()
wins = env.rollout(8, 100000)
end = time.time()
print(wins)
print(f"time taken: {end - start}, time per game: {(end - start) / 100000}")
