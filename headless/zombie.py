import json
from enum import Enum
from typing import List
import logging

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
        # self.pos = consts.OUT_OF_FIELD
        self.lane = None
        self.column = None
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
        target_plant = level.plant_grid[self.lane][self.column] # type: Plant
        if not target_plant: # Might be None if there's no plant there
            self.last_attack = level.frame
            return
        target_plant.hp -= self.damage
        logging.debug(f"[{level.frame}] Zombie in {self.lane, self.column} Attacked.")
        if target_plant.hp <= 0:
            level.plants.remove(target_plant)
            level.plant_grid[self.lane][self.column] = None
            logging.debug(f"[{level.frame}] Plant in {self.lane, self.column} was killed.")
            

    def move(self, level: "Level"):
        if (level.frame - self.last_moved) < self.move_interval * level.fps:
            return
        # if self.last_attack == level.frame: # if attacked this frame, reset move countdown and stay in place
        #     self.last_moved = level.frame
        #     return
        self.last_moved = level.frame
        # self.last_attack = level.frame # TODO - consider this, to let the zombie prepare for the first attack 
        level.zombie_grid[self.lane][self.column].remove(self)
        self.column -= 1
        logging.debug(f"[{level.frame}] Zombie in {self.lane, self.column + 1} moved to {self.lane, self.column}.")
        
        if self.column < 0:
            level.zombies.remove(self)
            if level.lawnmowers[self.lane] == True:
                logging.debug(f"[{level.frame}] Zombie in {self.lane, self.column} triggered a lawnmower.")
                level.lawnmowers[self.lane] = False
            else:
                logging.debug(f"[{level.frame}] Zombie in {self.lane, self.column} has killed you!")
                level.done = True
                level.win = False
        else:
            level.zombie_grid[self.lane][self.column].append(self)
        
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
