import json
from enum import Enum
from typing import List

import consts
if consts.TYPECHECK:
    from level import Level
    from plant import Plant


with open(consts.ZOMBIE_STATS_FILE_PATH, "r") as zombie_stats_file:
    zombie_stats = json.load(zombie_stats_file)


class zombie_type_to_filename(Enum):
    normal = "normal_zombie.json"
    conehead = "conehead_zombie.json"
    buckethead = "buckerhead_zombie.json"
    newspaper = "newspaper_zombie.json"


class Zombie():
    """
    TODO: Check if Subclassing is needed or if can get away with stats (newspaper zombie probably fucks this up)
    """
    def __init__(self, zombie_type):
        self.pos = consts.OUT_OF_FIELD
        self.move_interval = None
        self.last_moved = 0
        self.attack_interval = None
        self.last_attack = 0
        self.damage = None
        self.hp = None
        self.type = zombie_type
        self.status = None
        self.__dict__.update(zombie_stats[zombie_type])


    def attack(self, level: "Level"):
        if (level.frame - self.last_attack) < self.attack_interval * level.fps:
            return
        x, y = self.pos
        target_plant = level.plant_grid[x][y] # type: Plant
        if not target_plant: # Might be None if there's no plant there
            self.last_attack = level.frame
            return
        target_plant.hp -= self.damage
        if target_plant.hp <= 0:
            level.plants.remove(target_plant)
            level.plant_grid[x][y] = None

    def move(self, level: "Level"):
        if (level.frame - self.last_moved) < self.move_interval * level.fps:
            return
        # if self.last_attack == level.frame: # if attacked this frame, reset move countdown and stay in place
        #     self.last_moved = level.frame
        #     return
        self.last_moved = level.frame
        x, y = self.pos
        level.zombie_grid[x][y].remove(self)
        self.pos[1] -= 1
        if self.pos[1] < 0:
            level.zombies.remove(self)
            if level.lawnmowers[x] == True:
                level.lawnmowers[x] = False
            else:
                level.done = True
                level.win = False
        else:
            level.zombie_grid[x][y - 1].append(self)
        
    def __repr__(self):
        """
        Return a dict (?) describing this zomble.
        format:
        {
            "type": "zombie",
            "subtype": <specific type of zombie>,
            "hp": reminaing hp (int),
            "status": one of: [None, frozen, <other statuses?>]
        }
        """
        repr_dict = {
            "type": "zombie",
            "subtype": self.type,
            "hp": self.hp,
            "status": self.status
        }
        return repr_dict
    
    # def load_stats(self, stats_path):
    #     """
    #     Zombie stats json should be a dict with the following fields:
    #     "move_interval": number of frames to move a single square (secs to move a square * 60)
    #     "attack_interval": number of frames to attack
    #     "attack": How much damage does the zombe do
    #     "hp": health points of the zomb
    #     """
    #     stats_file = open(stats_path, "r")
    #     stats_json = json.load(stats_file)
    #     self.__dict__.update(stats_json)
