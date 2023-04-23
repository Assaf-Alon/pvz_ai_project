import numpy as np
import itertools
import json

import consts
from zombie import Zombie
from plant import Plant, Bullet

class Level():
    """
    This is the Env, generated each episode.
    A Level starts from scratch (as in the regular game).
    A Level gets it's zomble spawn times at __init__, from json or at random (this will be a flag for Level.__init__())

    As a general rule, the 2D grids unpack in the following way:
    grid[height][width]. For example:
    grid[3][2] means the square that's fourth from the top and third from the left.
    grid[0] means the top row.
    
    Note: Right now, it's the responsibility of the attacker to remove the object it attacked from all data structures if needed.

    TODO: Carefully consider the right Data structures to use for efficient management of objects in the environment. Check out dicts - O(1) removal
    """
    def __init__(self, length, height, level_data: dict, random = False, fps = 30):
        # Technical data:
        self.fps = fps
        self.frame = 0
        self.height = height # type: int
        self.length = length # type: int
        self.done = False
        self.win = False
        self.suns = 0 # Bank value
        # Object data
        self.zombies = [] # type: list[Zombie]
        self.plants = [] # type: list[Plant]
        self.active_suns = []
        self.bullets = [] # type: list[Bullet]
        self.lawnmowers = [True] * height
        self.zombie_grid = [[[] for _ in length] for _ in height] # type: list[list[list[Zombie]]]
        self.plant_grid = [[None for _ in length] for _ in height] # type: list[list[Plant]]
        if random:
            #TODO: Randomize level
            pass
        else:
            self.level_data = level_data # type: dict

    def assign_zombie_damage(self):
        for zombie in self.zombies:
            zombie.attack(self)

    def assign_plant_damage(self):
        for plant in self.plants:
            plant.attack(self)

    def move_zombies(self):
        for zombie in self.zombies:
            zombie.move(self)

    def spawn_zombies(self):
        """
        level_data should be a dict of the following format:
        "frame number": [[zombie_type, zombie_x], [zombie_type, zombie_x]]
        for example:
        600: [[normal, 0], [conehead, 3], [buckethead, 5]]
        """
        if self.frame in self.level_data.keys():
            for zombie_type, x in self.level_data[self.frame]:
                new_zombie = Zombie(zombie_type)
                new_zombie.pos = [x, self.length]
                # TODO - Add Zombie to zombies and/or zombies_grid?

    def spawn_suns(self):
        pass

    def do_player_action(self, action):
        # Need a way to check if the action is legal BEFORE it's attempted!
        pass

    def construct_state(self):
        # grid = 
        pass

    def step(self, action):
        """
        The main function of the environment ("Level")
        Every time step() is called, (at least) the following must happen:
        1. Zombies assign damage and move
        2. Plants assign damage
        4. New zombs are generated (as needed)
        5. Suns are generated (as objects? straight into bank? Maybe leave this as a setting of the Level __init__)
        6. Player can use oprerators to interact with env
        Note: one step corresponds to one frame (in a 60 fps game). As such, things wont acutally happen at every step.
        For example, plants will attack every ~60-120 frames (depending on plant), suns are auto-generated every ~600 frames 
        """
        self.frame += 1
        self.assign_zombie_damage()
        self.assign_plant_damage()
        self.move_zombies()
        self.spawn_zombies()
        self.spawn_suns()
        self.do_player_action(action)
        return self.suns, self.done, self.win
        # TODO: return state
