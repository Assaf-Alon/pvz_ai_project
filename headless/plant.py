import json
from enum import Enum

import consts
# from zombie import Zombie
# from level import Level

with open(consts.PLANT_STATS_FILE_PATH, "r") as plant_stats_file:
    plant_stats = json.load(plant_stats_file)
         

class Bullet():
    """
    This class represents a bullet fired by a plant.
    It has a single action: attack_or_move, which tries to hit a zombie if it's in the same square, or moves otherwise.
    """
    def __init__(self, lane: int, column: int, damage, move_interval = 20, pierce = 0):
        # TODO: Set a default move_interval, I think theyre all the same?
        self.lane = lane
        self.column = column
        self.move_interval = move_interval # how many frames to move a grid square
        self.last_moved = 0
        self.damage = damage
        self.pierce = pierce
    
    def attack_or_move(self, level: "Level"):
        pass

class Pea(Bullet):
    def __init__(self, lane: int, column: int, damage, move_interval = 20, pierce = 0):
        super().__init__(lane, column, damage)
    
    def attack_or_move(self, level: "Level"):
        x, y = self.lane, self.column
        if level.zombie_grid[x][y]: # attack
            target_zombie = level.zombie_grid[x][y][0] # type: Zombie
            target_zombie.hp -= self.damage
            if target_zombie.hp <= 0: # delete zomble from existence
                level.zombies.remove(target_zombie)
                level.zombie_grid[x][y].remove(target_zombie)
            # TODO: Piercing???
            level.bullets.remove(self) # remove self from bullet list after hitting zomble
        else: # move
            if (level.frame - self.last_moved) >= self.move_interval * level.fps:
                self.last_moved = level.frame
                self.column += 1 # TODO: Make sure we need the y coord, and not the x coord
                if self.column >= level.length: # bullet flew off the map
                    level.bullets.remove(self)


class Plant():
    def __init__(self, x, y):
        self.position = [x, y]
        self.cost = None
        self.hp = None
        self.damage = None
        self.attack_interval = None
        self.last_attack = 0

    def attack(self, level: "Level"):
        # Virtual function
        pass

    def generate_sun(self, level: "Level"):
        # Virtual func
        pass

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
    def __init__(self, x, y):
        super().__init__(x, y)
        self.last_sun_generated = 0
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
            level.active_suns.append([self.position]) # place sun object on field

class Peashooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.load_stats("peashooter")
    
    def attack(self, level: "Level"):
        if (level.frame - self.last_attack) < self.attack_interval * level.fps:
            return
        self.last_attack = level.frame
        pea = Pea(self.position[0], self.position[1] , self.damage)
        level.bullets.append(pea)

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
    
    
def create_plant_instance(plant_name, x, y):
    if plant_name == "sunflower":
        return Sunflower(x, y)
    elif plant_name == "peashooter":
        return Peashooter(x, y)
    
    