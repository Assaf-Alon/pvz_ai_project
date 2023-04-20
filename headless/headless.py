import numpy as np
import itertools
import json

import consts


class Level():
    """
    This is the Env, generated each episode.
    A Level starts from scratch (as in the regular game).
    A Level gets it's zomble spawn times at __init__, from json or at random (this will be a flag for Level.__init__())

    TODO: Carefully consider the right Data structures to use for efficient management of objects in the environment.
    """
    def __init__(self, length, height):
        self.frame = 0
        self.height = height
        self.length = length
        self.zombies = []
        self.plants = []
        self.suns = []
        # self.grid = [[{"plant": None, "zombies": [], "suns": []} for _ in length] for _ in height]
        self.zombie_grid = [[[] for _ in length] for _ in height] # a square may contain multiple zombs
        self.plant_grid = [[None for _ in length] for _ in height] # a square may contain a single plant
        # self.sun_grid = [] # Implement later, less critical

    def step(self, action):
        """
        The main function of the environment ("Level")
        Every time step() is called, (at least) the following must happen:
        1. Zombies assign damage and move
        2. Plants assign damage
        3. Everything that should have died, dies (this could be merged with 1 and 2, or left as a seperate func)
        4. New zombs are generated (as needed)
        5. Suns are generated (as objects? straight into bank? Maybe leave this as a setting of the Level __init__)
        6. Player can use oprerators to interact with env
        Note: one step corresponds to one frame (in a 60 fps game). As such, actions wont happen every step.
        For example, plants will attack every ~60-120 frames (depending on plant), suns are auto-generated every ~600 frames 
        """
        self.frame += 1

        zombie_damage_grid = np.zeros((self.height, self.length), dtype=np.uint8)
        for zombie in self.zombies:
            x, y = zombie.update_pos(self.step_num)
            zombie_damage_grid[x][y] += zombie.damage

        plant_damage_grid = np.zeros((self.height, self.length), dtype=np.uint8)
        for plant in self.plants:
            # this needs numpy to work
            # plant_damage_grid = np.add(plant_damage_grid, plant.attack(self.step_num))
            plant.attack(self.step_num, self.zombie_grid)

        for row, col in list(itertools.product(range(self.height), range(self.length))):
            self.plant_grid[row][col] -= zombie_damage_grid[row, col]

        
            



class Plant():
    def __init__(self, x, y):
        self.position = consts.OUT_OF_FIELD
        self.cost = None
        self.hp = None
        self.damage = None
        self.attack_interval = None
        self.last_attack = 0

    def plant(self, x, y):
        global suns
        if self.cost < suns:
            suns -= self.cost
            self.position = (x, y)
            return True
        else:
            return False
    
    def __sub__(self, x):
        self.hp -= x
        if self.hp <= 0:
            self.position = consts.OUT_OF_FIELD

    def attack(self, step_num, zombie_grid):
        pass

    def load_stats(self, stats_path):
        stats_file = open(stats_path, "r")
        stats_json = json.load(stats_file)
        self.__dict__.update(stats_json)
        

class Sun(Plant):
    def __init__(self):
        super(self, Plant).__init__()
        self.cost = 100

class PeaShooter(Plant):
    def __init__(self):
        super(self, Plant).__init__()
        self.load_stats()
    
    # normal attack: attack first zombie in row after own pos
    def attack(self, step_num, zombie_grid):
        # attack only if enough steps passed from last attack
        if not (step_num - self.last_attack) >= self.attack_interval:
            return
        row_num = self.pos[0]
        zombie_row = zombie_grid[row_num]
        # try to attack first zombie in row after own position
        for tile in zombie_row[self.pos[1]:]:
            if tile:
                first_zombie = tile[0]
                first_zombie -= self.damage
                break

class Zombie():
    def __init__(self):
        self.pos = consts.OUT_OF_FIELD
        self.move_interval = None
        self.damage = None
        self.hp = None

    def update_pos(self, step_num):
        if step_num % self.move_interval == 0:
            self.pos[1] -= 1
    
    def load_stats(self, stats_path):
        stats_file = open(stats_path, "r")
        stats_json = json.load(stats_file)
        self.__dict__.update(stats_json)

class NormalZombie(Zombie):
    def __init__(self):
        super(self, Zombie).__init__()
        self.load_stats("normal_zombie.json")
    