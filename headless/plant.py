import json
from enum import Enum
from itertools import product

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
        if self.pierce: # Attack all zombies in the grid square
            for target_zombie in level.zombie_grid[self.lane][self.column][:]: # Shallow copy to remove items while iterating
                target_zombie.get_damaged(self.damage, level)
        else: # Attack first zombie in grid square, then delete self
            target_zombie = level.zombie_grid[self.lane][self.column][0] # type: Zombie
            target_zombie.get_damaged(self.damage, level)
            level.bullets.remove(self) # remove self from bullet list after hitting zomble
            logging.debug(f"[{level.frame}] {bullet_type} in {self.lane, self.column} removed.")

    def move(self, level: "Level"):
        if (level.frame - self.last_moved) < self.move_interval * level.fps:
            return
        bullet_type = type(self).__name__
        logging.debug(f"[{level.frame}] {bullet_type} in {self.lane, self.column} moved to {self.lane, self.column + 1}.")
        self.last_moved = level.frame
        self.column += 1
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
            

class Lawnmower(Bullet):
    def __init__(self, lane: int, column = 0, damage=9999, move_interval = 20, pierce = True):
        super().__init__(lane, column, damage, pierce=pierce)

class Pea(Bullet):
    def __init__(self, lane: int, column: int, damage, move_interval = 20, pierce = False):
        super().__init__(lane, column, damage)
    

class Plant():
    def __init__(self, lane, column):
        """
        The following stats are shared between all plant types:
        lane, column, cost, hp, type (TODO: remove type and use self.__name__)
        """
        self.lane = lane
        self.column = column
        self.cost = None
        self.hp = None
        self.recharge = 0
        # self.type = plant_type
    
    def do_action(self, level: "Level"):
        # Virtual func
        # Represents attacking, generating a sun, exploding, doing nothing, etc.
        pass

    def get_damaged(self, damage, level: "Level"):
        self.hp -= damage
        logging.debug(f"[{level.frame}] {type(self).__name__} in {self.lane, self.column} got damaged. HP: {self.hp}")
        if self.hp <= 0:
            self.die(level)
            logging.debug(f"[{level.frame}] {type(self).__name__} in {self.lane, self.column} died.")
    
    def die(self, level: "Level"):
        level.plants.remove(self)
        level.plant_grid[self.lane][self.column] = None

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
            "subtype": type(self).__name__,
            "hp": self.hp,
        }
        return repr_dict    

    def load_stats(self):
        """
        Plant stats json should be a dict with the following fields:
        "attack_interval": number of frames to attack
        "attack": How much damage does the plant do
        "hp": health points of the plant
        "cost": how many suns does this plant cost
        # TODO: "refund": how many suns when selling plant
        """
        self.__dict__.update(plant_stats[type(self).__name__]) # lmao this is evil
        
class ShooterPlant(Plant):
    """
    Virtual class representing a plant that attacks by shooting
    Do not create instances of this class!
    """
    def __init__(self, lane, column, frame):
        super().__init__(lane, column)
        self.damage = 0
        self.attack_interval = 0
        self.last_attack = frame
        self.bullet_type = None # Class of bullet

    def shoot(self, level: "Level"):
        """
        Basic shooter type, some plants will need to override this
        """
        if (level.frame - self.last_attack) < self.attack_interval * level.fps:
            return

        self.last_attack = level.frame
        bullet = self.bullet_type(self.lane, self.column, self.damage, level.frame)
        level.bullets.append(bullet)
        logging.debug(f"[{level.frame}] {self.bullet_type.__name__} generated by {type(self).__name__} in {self.lane, self.column}.")

    def do_action(self, level: "Level"):
        self.shoot(level)


class MinePlant(Plant):
    def __init__(self, lane, column, frame):
        super().__init__(lane, column)
        self.attack = 0
        self.frame_planted = frame
        self.arming_interval = 0
        self.armed = False # Ready to boom?
        self.trigger_type = "zombie" # either zombie (when zombie gets close enough) or timer type triggers
        self.trigger_pos = [[0, 0], [0, 1]] # adds to position define which squares trigger explosion
        self.aoe = {
            "up": 0,
            "down": 0,
            "left": 0,
            "right": 0
        } # how many squares in each direction to damage
    
    def should_explode(self, level: "Level"):
        if not self.armed:
            return False
        
        if self.trigger_type == "zombie":
            if not any([level.zombie_grid[self.lane + pos[0]][self.column + pos[1]] for pos in self.trigger_pos]):
                return False
        
        return True
    
    def explode(self, level: "Level"):
        # fuck this dont make it generic
        if not self.armed:
            return
        
        if self.trigger_type == "zombie":
            if not any([level.zombie_grid[self.lane + pos[0][self.column + pos[1]]] for pos in self.trigger_pos]):
                return

        attacked_squares = []
        squares = list(product(range(level.lanes), range(level.columns)))
        for square in squares: # TODO: figure out if there's a more efficient way to do this.
            # remove square if lane is out of range
            if square[0] > self.lane + self.aoe['down'] or square[0] < self.lane - self.aoe['up']:
                return
            # remove square if column is out of range
            if square[1] > self.column + self.aoe['right'] or square[1] < self.column - self.aoe['left']:
                return
            attacked_squares += square
        for square in attacked_squares:
            lane, column = square
            for target_zombie in level.zombie_grid[lane][column][:]: # shallow copy to remove items while iterating
                target_zombie.hp -= self.attack
                if target_zombie.hp <= 0:
                    level.zombies.remove(target_zombie)
                    level.zombie_grid[lane][column].remove(target_zombie)
        
        level.plants.remove(self)
        level.plant_grid[self.lane][self.column] = None

    def arm(self, level: "Level"):
        if (level.frame - self.frame_planted) < self.arming_interval * level.fps:
            return
        
        if self.armed == False:
            logging.debug(f"[{level.frame}] {type(self).__name__} in {self.lane, self.column} is armed!")
            
        self.armed = True

    def do_action(self, level: "Level"):
        self.arm(level)
        self.explode(level)


class WallPlant(Plant):
    def __init__(self, lane, column, frame):
        super().__init__(lane, column)
        # No additional stats for you
    
    def do_action(self, level: "Level"):
        # Doesn't actually do anything
        pass

class SunPlant(Plant):
    def __init__(self, lane, column, frame):
        super().__init__(lane, column)
        self.last_sun_generated = frame
        self.sun_interval = 0
        self.sun_value = 0

    def generate_sun(self, level: "Level"):
        if (level.frame - self.last_sun_generated) < self.sun_interval * level.fps:
            return
        self.last_sun_generated = level.frame
        if consts.AUTO_COLLECT:
            level.suns += self.sun_value # add sun straight to bank
        else:
            level.active_suns.append([self.lane, self.column]) # place sun object on field
        logging.debug(f"[{level.frame}] Sun generated by Sunflower in {self.lane, self.column}. Total: {level.suns}.")

    def do_action(self, level: "Level"):
        self.generate_sun(level)


class Sunflower(SunPlant):
    def __init__(self, lane, column, frame):
        super().__init__(lane, column, frame)
        self.load_stats()


class Peashooter(ShooterPlant):
    def __init__(self, lane, column, frame):
        super().__init__(lane, column, frame)
    # def __init__(self, plant_type, lane, column, frame):   # TODO What is plant_type? ShooterPlant doesn't seem to expect it
    #     super().__init__(plant_type, lane, column, frame)
        self.load_stats()
        self.bullet_type = Pea


class PotatoMine(MinePlant):
    def __init__(self, lane, column, frame):
        super().__init__(lane, column, frame)
        self.load_stats()
        # Stats
    
    # TODO - make the potatomine immortal once armed
    # def arm(self, level: "Level"):
    #     super().arm(level)
    #     if self.armed:
    #         self.hp = math.inf
        

    def explode(self, level: "Level"):
        if not super().should_explode(level):
            return
        logging.debug(f"[{level.frame}] {type(self).__name__} in {self.lane, self.column} is preparing to explode.")
        for column in range(self.column, self.column + 2):
            for target_zombie in level.zombie_grid[self.lane][column][:]: # shallow copy to remove items while iterating
                target_zombie.get_damaged(self.damage, level)
        level.plants.remove(self)
        level.plant_grid[self.lane][self.column] = None
        logging.debug(f"[{level.frame}] {type(self).__name__} in {self.lane, self.column} has exploded.")
        


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

class WallNut(WallPlant):
    def __init__(self, lane, column, frame):
        super().__init__(lane, column, frame)
        self.load_stats()

class name_to_class(Enum):
    peashooter = Peashooter
    sunflower = Sunflower
    potatomine = PotatoMine
    
    
def create_plant_instance(plant_name, lane, column, frame):
    if plant_name == "Sunflower":
        return Sunflower(lane, column, frame)
    elif plant_name == "Peashooter":
        return Peashooter(lane, column, frame)
    elif plant_name == "WallNut":
        return WallNut(lane, column, frame)
    elif plant_name == "PotatoMine":
        return PotatoMine(lane, column, frame)
    else:
        # TODO - implement default?
        from inspect import currentframe, getframeinfo
        frameinfo = getframeinfo(currentframe())
        print(f"DUDE!! WHAT THE HELL IS {plant_name.upper()}?!")
        print(f"Add this plant to {frameinfo.filename}, line {frameinfo.lineno - 3} ")
        exit(1)