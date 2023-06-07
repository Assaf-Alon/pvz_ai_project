import cpp_env.level as cpp_level
import utils

lanes = 5
cols = 10
num_rollouts = 1000

class node:
    def __init__(self, level: cpp_level.Level, action: cpp_level.Action):
        self.children = {}
        self.level = level.clone() # type: cpp_level.Level
        while not self.level.is_action_legal(action.plant_name, action.lane, action.col):
            self.level.step() # empty step
            if self.level.done:
                self.leaf = True
                self.wins = self.level.win * num_rollouts
                self.total_rollouts = num_rollouts
                return
        # while (position := self.level.get_random_position()) == (-1, -1):
        #     self.level.step()
        #     if self.level.done:
        #         self.leaf = True
        #         self.wins = self.level.win * num_rollouts
        #         self.total_rollouts = num_rollouts
        #         return
        self.level.step(action.plant_name, action.lane, action.col)
        self.do_rollouts()

    def select_next_node():
        pass

    def expand(self):
        pass

    def do_rollouts(self):
        self.wins = self.level.rollout(8, num_rollouts)
        self.total_rollouts = num_rollouts
        self.ucb = ...


if __name__ == "__main__":
    level = cpp_level.Level(5, 10, 10, utils.level_data_1, utils.chosen_plants_basic)
    test_node = node(level, cpp_level.Action(cpp_level.SUNFLOWER, 2,3))
    print(f"rollouts: {test_node.total_rollouts}, wins: {test_node.wins}")
    
"""
steps:
1. choose a node according to UCB
2. Expand node using a list of random (legal) actions
3. rollout expanded nodes
4. update self ucb using child wins, plays
"""