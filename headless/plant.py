import json
from enum import Enum

import logging
import consts
if consts.TYPECHECK:
    from zombie import Zombie
    from level import Level

with open(consts.PLANT_STATS_FILE_PATH, "r") as plant_stats_file:
    plant_stats = json.load(plant_stats_file)
         

class Bullet():
    """
    This class represents a bullet fired by a plant.
    It has a single action: attack_or_move, which tries to hit a zombie if it's in the same square, or moves otherwise.
    """
    def __init__(self, lane: int, column: int, damage, move_interval = 0.2, pierce = False):
        # TODO: Set a default move_interval, I think they're all the same?
        self.lane = lane
        self.column = column
        self.move_interval = move_interval
        self.last_moved = 0
        self.damage = damage
        self.pierce = pierce
    
    def attack(self, level: "Level"):
        bullet_type = type(self).__name__
        logging.debug(f"[{level.frame}] {bullet_type} in {self.lane, self.column} attacked.")
        target_zombie = level.zombie_grid[self.lane][self.column][0] # type: Zombie
        target_zombie.hp -= self.damage
        logging.debug(f"[{level.frame}] Zombie in {self.lane, self.column} was damaged. HP: {target_zombie.hp}.")
        if target_zombie.hp <= 0: # delete zomble from existence
            logging.debug(f"[{level.frame}] Zombie in {self.lane, self.column} was killed.")
            level.zombies.remove(target_zombie)
            level.zombie_grid[self.lane][self.column].remove(target_zombie)
        # TODO: Piercing???
        if not self.pierce:
            level.bullets.remove(self) # remove self from bullet list after hitting zomble
            logging.debug(f"[{level.frame}] {bullet_type} in {self.lane, self.column} removed.")
            
    
    def move(self, level: "Level"):
        if (level.frame - self.last_moved) < self.move_interval * level.fps:
            return
        bullet_type = type(self).__name__
        logging.debug(f"[{level.frame}] {bullet_type} in {self.lane, self.column} moved to {self.lane, self.column + 1}.")
        self.last_moved = level.frame
        self.column += 1 # TODO: Make sure we need the y coord, and not the x coord
        if self.column >= level.columns: # bullet flew off the map
            level.bullets.remove(self)
            logging.debug(f"[{level.frame}] {bullet_type} in {self.lane, self.column} removed.")
        elif level.zombie_grid[self.lane][self.column]:
            self.attack(level)
    
    def attack_or_move(self, level: "Level"):
        if level.zombie_grid[self.lane][self.column]: # attack
            self.attack(level)
            if self.pierce:
                self.move(level)
        else:
            self.move(level)
            

class LawnMower(Bullet):
    def __init__(self, lane: int, column = -1, damage=10000, move_interval = 20, pierce = True):
        super().__init__(lane, column, damage, pierce=pierce)

class Pea(Bullet):
    def __init__(self, lane: int, column: int, damage, move_interval = 20, pierce = False):
        super().__init__(lane, column, damage)
    
    # def attack(self, level: "Level"): # TODO - consider merging this back to attack_or_move for better performance
    #     super().attack(level)
            
    # def attack_or_move(self, level: "Level"):
    #     super().attack_or_move(level)


class Plant():
    def __init__(self, plant_type, lane, column, frame):
        self.lane = lane
        self.column = column
        self.cost = None
        self.hp = None
        self.damage = None
        self.attack_interval = None
        self.last_attack = frame
        self.type = plant_type
        self.status = None

    def attack(self, level: "Level"):
        # Virtual function
        pass

    def generate_sun(self, level: "Level"):
        # Virtual func
        pass

    def __repr__(self):
        """
        Return a dict (?) describing this plant.
        format:
        {
            "type": "plant",
            "subtype": <specific type of plant>,
            "hp": reminaing hp (int),
            "status": one of: [None, low_suns (for shrooms), <other statusi>]
        }
        """
        repr_dict = {
            "type": "plant",
            "subtype": self.type,
            "hp": self.hp,
            "status": self.status
        }
        return repr_dict    

    def load_stats(self, plant_type):
        """
        Plant stats json should be a dict with the following fields:
        "attack_interval": number of frames to attack
        "attack": How much damage does the plant do
        "hp": health points of the plant
        "cost": how many suns does this plant cost
        # TODO: "refund": how many suns when selling plant
        """
        self.__dict__.update(plant_stats[plant_type])
        


class Sunflower(Plant):
    def __init__(self, plant_type, lane, column, frame):
        super().__init__(plant_type, lane, column, frame)
        self.last_sun_generated = frame
        self.sun_interval = None
        self.sun_value = None
        self.load_stats("sunflower")
    
    def generate_sun(self, level: "Level"):
        if (level.frame - self.last_sun_generated) < self.sun_interval * level.fps:
            return
        self.last_sun_generated = level.frame
        if consts.AUTO_COLLECT:
            level.suns += self.sun_value # add sun straight to bank
        else:
            level.active_suns.append([self.lane, self.column]) # place sun object on field
        logging.debug(f"[{level.frame}] Sun generated by Sunflower in {self.lane, self.column}. Total: {level.suns}.")

class Peashooter(Plant):
    def __init__(self, plant_type, lane, column, frame):
        super().__init__(plant_type, lane, column, frame)
        self.load_stats("peashooter")
    
    def attack(self, level: "Level"):
        if (level.frame - self.last_attack) < self.attack_interval * level.fps:
            return
        self.last_attack = level.frame
        pea = Pea(self.lane, self.column, self.damage)
        pea.last_moved = level.frame
        level.bullets.append(pea)
        logging.debug(f"[{level.frame}] Pea generated by Peashooter in {self.lane, self.column}.")

class PotatoMine(Plant):
    def __init__(self):
        super(self, Plant).__init__()
        self.load_stats()
        # Stats
    
class CherryBomb(Plant):
    pass

class Chomper(Plant):
    pass

class HypnoShroom(Plant):
    pass

class IceShroom(Plant):
    pass

class Japalapeno(Plant):
    pass

class PuffShroom(Plant):
    pass

class RepeaterPea(Plant):
    pass

class ScaredyShroom(Plant):
    pass

class SnowPea(Plant):
    pass

class Spikeweed(Plant):
    pass

class Squash(Plant):
    pass


class SunShroom(Plant):
    pass

class ThreePeater(Plant):
    pass

class WallNut(Plant):
    pass

class name_to_class(Enum):
    peashooter = Peashooter
    sunflower = Sunflower
    potatomine = PotatoMine
    
    
def create_plant_instance(plant_name, lane, column, frame):
    if plant_name == "sunflower":
        return Sunflower(plant_name, lane, column, frame)
    elif plant_name == "peashooter":
        return Peashooter(plant_name, lane, column, frame)
    
    