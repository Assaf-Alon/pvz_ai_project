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
        self.attack_interval = None
        self.last_action = 0
        self.damage = None
        self.hp = None
        self.type = zombie_type
        self.action_interval_modifier = 1 # Allows making zombie attack/move slower or faster
        self.status = {
            "frozen": 0, # value: frame frozen expires
            "hypnotized": False, # value: is hypnotized or not
        }
        self.__dict__.update(zombie_stats[zombie_type])
        self.reached_house = False # flag that marks zombie as having reached the lawnmower column

    def do_action(self, level: "Level"):
        """
        Zombie actions are attack if plant is there, move otherwise.
        """
        if self.status["frozen"] > level.frame: # frozen expired
            self.action_interval_modifier = 1

        self.attack(level)
        self.move(level)

    def attack(self, level: "Level"):
        if (level.frame - self.last_action) < self.attack_interval * level.fps * self.action_interval_modifier:
            return
        target_plant = level.plant_grid[self.lane][self.column] # type: Plant
        if not target_plant:
            return
        self.last_action = level.frame

        logging.debug(f"[{level.frame}] {self.type} zombie in {self.lane, self.column} attacked.")
        target_plant.get_damaged(self.damage, level)

    def move(self, level: "Level"):
        if (level.frame - self.last_action) < self.move_interval * level.fps * self.action_interval_modifier:
            return
        self.last_action = level.frame
        
        if self.column == 0: # If zombie wants to enter the house in this frame
            self.reached_house = True
            logging.debug(f"[{level.frame}] {self.type} zombie in {self.lane, self.column} attempted entering the house.")

        else:
            level.zombie_grid[self.lane][self.column].remove(self)
            self.column -= 1
            level.zombie_grid[self.lane][self.column].append(self)
            logging.debug(f"[{level.frame}] {self.type} zombie in {self.lane, self.column + 1} moved to {self.lane, self.column}.")

    def add_status(self, level: "Level", status: str):
        """
        Apply a status effect to the zombie
        """
        if status == "frozen":
            self.status["frozen"] = level.frame + 10 * level.fps
            self.action_interval_modifier = 2
        elif status == "hypnotized":
            self.status["hypnotized"] = True
            self.attack = self.hypnotized_attack
            self.move = self.hypnotized_move

    def hypnotized_attack(self, level: "Level"):
        if (level.frame - self.last_action) < self.attack_interval * level.fps * self.action_interval_modifier:
            return
        target_zombie_list = level.zombie_grid[self.lane][self.column] # type: List[Zombie]
        if not target_zombie_list:
            return
        self.last_action = level.frame

        target_zombie = target_zombie_list[0]
        logging.debug(f"[{level.frame}] Hypnotized {self.type} zombie in {self.lane, self.column} attacked another zombie!")
        target_zombie.get_damaged(self.damage, level)

    def hypnotized_move(self, level: "Level"):
        if (level.frame - self.last_action) < self.attack_interval * level.fps * self.action_interval_modifier:
            return
        self.last_action = level.frame

        if self.column == level.columns - 1:
            logging.debug(f"[{level.frame}] Hypnotized {self.type} zombie in {self.lane, self.column} has fell off the map!")
            self.die(level)
        else:
            level.zombie_grid[self.lane][self.column].remove(self)
            self.column -= 1
            level.zombie_grid[self.lane][self.column].append(self)
            logging.debug(f"[{level.frame}] Hypnotized {self.type} zombie in {self.lane, self.column + 1} moved to {self.lane, self.column}.")


    def get_damaged(self, damage, level: "Level"):
        self.hp -= damage
        logging.debug(f"[{level.frame}] {self.type} zombie in {self.lane, self.column} was damaged. HP: {self.hp}.")
        if self.type == "newspaper": # newspaper zombie gets damaged differently
            if self.hp <= self.newspaper_threshold: # attribute unique to this zombie type
                logging.debug(f"[{level.frame}] {self.type} zombie in {self.lane, self.column} lost his newspaper!")
                self.move_interval = self.no_newspaper_move_interval # attribute unique to this zombie type
                self.type = "no_newspaper"
        if self.hp <= 0:
            self.die(level)
    
    def die(self, level: "Level"):
        """
        Method to die if hp is zero. Will be called by either bullet or plant.
        """
        logging.debug(f"[{level.frame}] {self.type} zombie in {self.lane, self.column} was killed.")
        level.zombies.remove(self)
        level.zombie_grid[self.lane][self.column].remove(self)
        
    def __repr__(self):
        """
        Return a dict (?) describing this zomble.
        format:
        {
            "type": "zombie",
            "subtype": <specific type of zombie>,
            "hp": reminaing hp (int),
            "status": list of active statuses affecting this zombe (i.e. frozen, hypnotized)
        }
        """
        active_statuses = []
        for key, value in self.status.items():
            if value:
                active_statuses.append(key)
        repr_dict = {
            "type": "zombie",
            "subtype": self.type,
            "hp": self.hp,
            "status": active_statuses
        }
        return repr_dict
    
