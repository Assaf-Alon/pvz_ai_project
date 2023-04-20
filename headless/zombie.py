import json
from enum import Enum

import consts
from plant import Plant
from level import Level


class zombie_type_to_filename(Enum):
    normal = "normal_zombie.json"
    conehead = "conehead_zombie.json"
    buckethead = "buckerhead_zombie.json"
    newspaper = "newspaper_zombie.json"


class Zombie():
    def __init__(self, zombie_type):
        self.pos = consts.OUT_OF_FIELD
        self.move_interval = None
        self.last_moved = 0
        self.attack_interval = None
        self.last_attack = 0
        self.damage = None
        self.hp = None
        self.type = zombie_type
        self.load_stats(zombie_type_to_filename[zombie_type].value)

    def attack(self, frame, plant_grid: list[list[Plant]]):
        if (frame - self.last_attack) < self.attack_interval:
            return
        self.last_attack = frame
        x, y = self.pos
        target_plant = plant_grid[x][y] # type: Plant
        if not target_plant: # Might be None if there's no plant there
            return
        target_plant.hp -= self.damage

    def move(self, level: Level):
        if (level.frame - self.last_moved) < self.move_interval:
            return
        self.last_moved = level.frame
        x, y = self.pos
        level.zombie_grid[x][y].remove(self)
        self.pos[1] -= 1
        if self.pos[1] < 0:
            #TODO: Damage player or trigger lawnmower
            pass
        else:
            level.zombie_grid[x][y - 1].append(self)
    
    def load_stats(self, stats_path):
        """
        Zombie stats json should be a dict with the following fields:
        "move_interval": number of frames to move a single square (secs to move a square * 60)
        "attack_interval": number of frames to attack
        "attack": How much damage does the zombe do
        "hp": health points of the zomb
        """
        stats_file = open(stats_path, "r")
        stats_json = json.load(stats_file)
        self.__dict__.update(stats_json)

# class NormalZombie(Zombie):
#     def __init__(self):
#         super(self, Zombie).__init__()
#         self.load_stats("normal_zombie.json")