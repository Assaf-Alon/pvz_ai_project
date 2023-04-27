import numpy as np
import os
import itertools
import json
from typing import Dict, List
import time
import logging, sys

import consts
import utils
import zombie
import plant



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
    def __init__(self, columns, lanes, level_data: dict, random = False, fps = 30, logfile=consts.LOG_FILE_NAME):
        # Technical data:
        self.fps = fps
        self.frame = 0
        self.lanes = lanes # type: int
        self.columns = columns # type: int
        self.done = False
        self.win = False
        self.suns = 50 # Bank value
        
        # Object data
        self.replant_queue = {plant_name: 0 for plant_name in utils.get_plant_names()}
        self.plant_costs = utils.get_plant_costs()
        self.zombies = [] # type: list[zombie.Zombie]
        self.plants = [] # type: list[plant.Plant]
        self.active_suns = []
        self.bullets = [] # type: list[plant.Bullet]
        self.lawnmowers = [True] * lanes
        self.zombie_grid = [[[] for _ in range(columns)] for _ in range(lanes)] # type: list[list[list[zombie.Zombie]]]
        self.plant_grid = [[None for _ in range(columns)] for _ in range(lanes)] # type: list[list[plant.Plant]]
        
        # Internal data
        self.sun_value = 25
        self.last_sun_generated_frame = 0
        self.sun_interval = 10
        if random:
            #TODO: Randomize level
            pass
        else:
            self.level_data = level_data # type: dict
            self.zombies_to_be_spawned = utils.get_zombies_to_be_spawned(level_data)

        utils.configure_logging(logfile)
        
    def assign_zombie_damage(self):
        for zombie in self.zombies:
            zombie.attack(self)

    def assign_plant_damage(self):
        for plant in self.plants: # All plants try to shoot or attack
            plant.attack(self)
        
        # TODO - [note] We're copying the bullets array here because we're removing objects from it while iterating
        for bullet in self.bullets[:]: # All bullets either hit a target or move. New bullet can hit target on same frame as it's created
            bullet.attack_or_move(self)

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
        if not self.zombies_to_be_spawned:
            return
        
        curr_sec = str(self.frame // self.fps)
        next_spawn = self.zombies_to_be_spawned[0][0]
        if self.frame % self.fps == 0 and next_spawn == curr_sec:
            print(self.zombies_to_be_spawned)
            for zombie_type, lane in self.zombies_to_be_spawned[0][1]:
                new_zombie = zombie.Zombie(zombie_type)
                new_zombie.lane = lane
                new_zombie.column = self.columns - 1
                new_zombie.last_moved = self.frame
                # self.zombies[new_zombie] = new_zombie.pos
                self.zombies.append(new_zombie)
                self.zombie_grid[lane][self.columns - 1].append(new_zombie)
            self.zombies_to_be_spawned.popleft()

    def spawn_suns(self):
        if (self.frame - self.last_sun_generated_frame) > self.sun_interval * self.fps:
            self.last_sun_generated_frame = self.frame
            if consts.AUTO_COLLECT:
                self.suns += 25
            else:
                self.active_suns.append([0, 0]) # TODO: Randomize sun location
            logging.debug(f"[{self.frame}] Sun autospawned. Total: {self.suns}.")
        for plant in self.plants:
            plant.generate_sun(self)

    def activate_lawnmower(self, lane: int):
        self.bullets.append(plant.LawnMower(lane))
    
    def _is_plant_legal(self, plant_name: str, x, y):
        # Are the provided coords within the map?
        if x < 0 or x >= self.lanes or y < 0 or y >= self.columns:
            return False
        # TODO:
        # was this plant chosen for this run?
        # Location is free
        if self.plant_grid[x][y]:
            return False
        # There's no need to recharge
        if self.replant_queue[plant_name] > 0:
            return False
        # There's enough suns
        if self.suns < self.plant_costs[plant_name]:
            return False
        return True
        
    def action_is_legal(self, action): # This is for the player to check if he can do an action right now
        if not action:
            return True
        
        if action[0] == "plant":
            _, plant_name, x, y = action
            return self._is_plant_legal(plant_name, x, y)

        return False
        
    def plant(self, plant_name: str, x, y):
        if not self._is_plant_legal(plant_name, x, y):
            return
        # new_plant = plant.name_to_class[plant_name](x, y) # type: plant.Plant
        new_plant = plant.create_plant_instance(plant_name, x, y) # selector for correct type of subclass, check if this can be done more cleanly
        self.plants.append(new_plant)
        self.plant_grid[x][y] = new_plant
        self.suns -= new_plant.cost
        logging.debug(f"[{self.frame}] Planted {plant_name} in {x, y}. Total: {self.suns}.")
        
        
    def do_player_action(self, action: list):
        if not action:
            return
        # to plant a new plant, action must be of the form:
        # plant <plantname> <x coord> <y coord>
        # Example: ["plant", "peashooter", 2, 5]
        # Note! x, y coords must be integers
        if action[0] == "plant":
            _, plant_name, x, y = action
            self.plant(plant_name, x, y)

    def construct_state(self):
        grid = [[[] for _ in range(self.columns)] for _ in range(self.lanes)]
        for plant in self.plants:
            lane, column = plant.lane, plant.column
            grid[lane][column].append(plant.__repr__())
        for zombie in self.zombies:
            grid[zombie.lane][zombie.column].append(zombie.__repr__())
        state_tuple = (self.suns, self.lawnmowers, grid)
        return state_tuple

    def step(self, action: str):
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
        return self.construct_state()
        # TODO: return state

    def print_grid(self):
        os.system('clear')
        for row in range(self.lanes):
            print("-" * (4 * self.lanes))
            for col in range(self.columns):
                cell_content = ["0", "0", "0"]  # Plants, Bullets, Zombies
                if self.plant_grid[row][col]:
                    if type(self.plant_grid[row][col]) == plant.Peashooter:
                        cell_content[0] = "P"
                    if type(self.plant_grid[row][col]) == plant.Sunflower:
                        cell_content[0] = "S"
                if self.zombie_grid[row][col]:
                    cell_content[2] = len(self.zombie_grid[row][col])
                for bullet in self.bullets:
                    if bullet.position == (row, col):
                        cell_content[1] += 1
                print(f"| {cell_content[0]}{cell_content[1]}{cell_content[2]} ", end='')
            print("|")
        print("-" * (4 * self.columns))
                
                
                
    # def print_board(matrix):
    # for row in matrix:
    #     print("-" * (4 * len(row) + 1))  # Print horizontal line
    #     for element in row:
    #         print("|", f" {element} ", end='')  # Print element with vertical lines
    #     print("|")  # Print closing vertical line
    # print("-" * (4 * len(matrix[0]) + 1))  # Print bottom horizontal line
