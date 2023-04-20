import json

import consts
from zombie import Zombie
from level import Level

            
class Bullet():
    """
    This class represents a bullet fired by a plant.
    It has a single action: attack_or_move, which tries to hit a zombie if it's in the same square, or moves otherwise.
    """
    def __init__(self, position: list, damage, move_interval = 20, pierce = 0):
        # TODO: Set a default move_interval, I think theyre all the same?
        self.position = position
        self.move_interval = move_interval # how many frames to move a grid square
        self.last_moved = 0
        self.damage = damage
        self.pierce = pierce
    
    def attack_or_move(self, level: Level):
        pass

class Pea(Bullet):
    def __init__(self, position: list, damage, move_interval = 20, pierce = 0):
        super(self, Bullet).__init__(position, damage)
    
    def attack_or_move(self, level: Level):
        x, y = self.position
        if level.zombie_grid[x][y]:
            target_zombie = level.zombie_grid[x][y][0] # type: Zombie
            target_zombie.hp -= self.damage
            if target_zombie.hp <= 0: # delete zomble from existence
                level.zombies.remove(target_zombie)
                level.zombie_grid[x][y].remove(target_zombie)
            # TODO: Piercing???
            level.bullets.remove(self) # remove self from bullet list after hitting zomble
        else:
            if (level.frame - self.last_moved) >= self.move_interval:
                self.last_moved = level.frame
                self.position[1] += 1 # TODO: Make sure we need the y coord, and not the x coord
                if self.position[1] >= level.length: # bullet flew off the map
                    level.bullets.remove(self)


class Plant():
    def __init__(self, x, y):
        self.position = [x, y]
        self.cost = None
        self.hp = None
        self.damage = None
        self.attack_interval = None
        self.last_attack = 0

    def plant(self, level: Level, x, y):
        # TODO: Nasty
        global suns
        if self.cost < suns:
            suns -= self.cost
            self.position = (x, y)
            return True
        else:
            return False

    def attack(self, level: Level):
        # Virtual function
        pass

    def load_stats(self, stats_path):
        """
        Plant stats json should be a dict with the following fields:
        "attack_interval": number of frames to attack
        "attack": How much damage does the plant do
        "hp": health points of the plant
        "cost": how many suns does this plant cost
        # TODO: "refund": how many suns when selling plant
        """
        stats_file = open(stats_path, "r")
        stats_json = json.load(stats_file)
        self.__dict__.update(stats_json)
        

class Sunflower(Plant):
    def __init__(self, x, y):
        super(self, Plant).__init__(x, y)
        self.cost = 100

class Peashooter(Plant):
    def __init__(self):
        super(self, Plant).__init__()
        self.load_stats()
    
    def attack(self, level: Level):
        if (level.frame - self.last_attack) < self.attack_interval:
            return
        self.last_attack = level.frame
        pea = Pea(self.position, self.damage)
        level.bullets.append(pea)
