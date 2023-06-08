import cpp_env.level as cpp_level
import utils
import numpy as np

lanes = 5
cols = 10
size_expand = 100
num_rollouts = 1000
chosen_plants = utils.chosen_plants_1



# def generate_all_actions(level: cpp_level.Level):
#     free_spaces = level.get_all_legal_positions() # type: list[tuple[int, int]]
#     plantable_plants = chosen_plants
#     legal_actions = ...

class node:
    def __init__(self, level: cpp_level.Level, action: cpp_level.Action):
        self.children = {}
        self.level = level.clone() # type: cpp_level.Level
        while not self.level.is_action_legal(action):
            self.level.step() # empty step
            if self.level.done:
                self.leaf = True
                self.wins = self.level.win * num_rollouts
                self.total_rollouts = num_rollouts
                return
        self.level.step(action)
        self.do_rollouts()

    def select_next_node():
        pass

    def expand(self, get_random_action: callable):
        """
        Create {size_expand} child nodes with unique random actions
        """
        for _ in range(size_expand):
            # while (action := self.level.get_random_action()) in self.children.keys(): pass
            while (action := get_random_action()) in self.children.keys(): pass
            self.children[action] = node(self.level, action)
            self.total_rollouts += self.children[action].total_rollouts
            self.wins += self.children[action].wins

    def do_rollouts(self):
        self.wins = self.level.rollout(8, num_rollouts)
        self.total_rollouts = num_rollouts
        self.ucb = ...

class MCTS:
    def __init__(self, level_data: cpp_level.ZombieQueue, chosen_plants: list[int]):
        self.chosen_plants = chosen_plants
        self.level = cpp_level.Level(lanes, cols, 10, level_data, chosen_plants)
        self.root = node(self.level, cpp_level.Action(0, 0, 0))
        self.children = {}

    def random_action_function_factory(self): # allowed to be illegal
        lanes = self.level.lanes
        cols = self.level.cols
        chosen_plants = self.chosen_plants
        def random_action():
            lane = np.random.randint(0, lanes)
            col = np.random.randint(0, cols)
            plant = np.random.randint(0, len(chosen_plants))
            return cpp_level.Action(chosen_plants[plant], lane, col)
        return random_action


    def run(self):
        pass

    def root_expand(self): # test func dont actually do it like this
        self.root.expand(self.random_action_function_factory())


if __name__ == "__main__":
    mcts = MCTS(utils.level_data_1, chosen_plants)
    test_node = mcts.root
    print(f"rollouts: {test_node.total_rollouts}, wins: {test_node.wins}")
    mcts.root_expand()
    print(f"rollouts: {test_node.total_rollouts}, wins: {test_node.wins}")
    for action, child in sorted(test_node.children.items(), key=lambda x: x[1].wins, reverse=True):
        print(f"action: {mcts.level.plant_data[action.plant_name].plant_name} at {action.lane}, {action.col}, rollouts: {child.total_rollouts}, wins: {child.wins}")

    
"""
steps:
1. choose a node according to UCB
2. Expand node using a list of random (legal) actions
3. rollout expanded nodes
4. update self ucb using child wins, plays
"""