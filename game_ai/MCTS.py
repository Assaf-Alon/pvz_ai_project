import cpp_env.level as cpp_level
import utils
import numpy as np
import itertools
import numba
import time

lanes = 5
cols = 10
size_expand = 100
num_rollouts = 100
chosen_plants = utils.chosen_plants_1
UCB_C = 1.41

@numba.jit(nopython=True)
def calculate_ucb(wins: int, plays: int, parent_plays: int):
    if plays == 0:
        return np.inf
    return (wins / plays) + (UCB_C * np.sqrt(np.log(parent_plays) / plays))

# def generate_all_actions(level: cpp_level.Level):
#     free_spaces = level.get_all_legal_positions() # type: list[tuple[int, int]]
#     plantable_plants = chosen_plants
#     legal_actions = ...

class node:
    def __init__(self, level: cpp_level.Level, action: cpp_level.Action, parent: "node" = None):
        self.parent = parent # type: node
        self.children = {} # dict[cpp_level.Action, node]
        self.level = level.clone() # type: cpp_level.Level
        while not self.level.is_action_legal(action):
            self.level.step() # empty step
            if self.level.done:
                self.wins = self.level.win * num_rollouts
                self.total_rollouts = num_rollouts
                self.ucb = self.level.win
                return
        self.level.step(action)
        self.do_rollouts()

    def select_next_node(self):
        for action, child in sorted(self.children.items(), key=lambda x: x[1].ucb, reverse=True):
            if child.level.done:
                continue
            if len(child.children) == 0:
                return child
            return child.select_next_node()
        return self

    def expand(self, actions: itertools.product):
        """
        Create {size_expand} child nodes with unique random actions
        Actions don't have to be legal, as the child nodes will simply do nothing until they can do the action
        """
        for action in actions:
            self.children[action] = node(self.level, cpp_level.Action(*action))
            self.total_rollouts += self.children[action].total_rollouts
            self.wins += self.children[action].wins

    def do_rollouts(self):
        self.wins = self.level.rollout(8, num_rollouts)
        self.total_rollouts = num_rollouts
        self.ucb = calculate_ucb(self.wins, self.total_rollouts, self.total_rollouts)

    def backpropagate(self, rollouts: int, wins: int):
        self.total_rollouts += rollouts
        self.wins += wins
        if self.parent is not None:
            self.parent.backpropagate(rollouts, wins) # recursion moment
            self.ucb = calculate_ucb(self.wins, self.total_rollouts, self.parent.total_rollouts)
        else:
            self.ucb = calculate_ucb(self.wins, self.total_rollouts, self.total_rollouts)


class MCTS:
    def __init__(self, level: cpp_level.Level):
        self.level = level.clone() # type: cpp_level.Level
        self.chosen_plants = level.chosen_plants
        self.root = node(self.level, cpp_level.Action(0, 0, 0))
        self.children = {}
        self.generate_all_actions()

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

    def generate_all_actions(self):
        self.actions = itertools.product(self.chosen_plants, range(self.level.lanes), range(self.level.cols))

    def run(self, time_left_secs: int):
        timeout = time.time() + time_left_secs
        while time.time() < timeout:
            next_node = self.root.select_next_node()
            next_node.expand(self.actions)
        best_action = cpp_level.Action(0,0,0)
        best_ucb = -1
        for action, child in self.root.children.items():
            if child.ucb > best_ucb:
                best_ucb = child.ucb
                best_action = action
        return best_action

    def root_expand(self): # test func dont actually do it like this
        self.root.expand(self.actions)


if __name__ == "__main__":
    level = cpp_level.Level(lanes, cols, 10, utils.lvl4_data, utils.chosen_plants_lvl4)
    backup_level = level.clone()
    step = 0
    actions_taken = []
    while not level.done:
        mcts = MCTS(level)
        chosen_action = mcts.run(1)
        print(f"simulations: {mcts.root.total_rollouts}")
        cpp_action = cpp_level.Action(*chosen_action)
        while not level.is_action_legal(cpp_action) and not level.done:
            level.step()
        if level.done:
            break
        actions_taken.append(chosen_action)
        print(f"skipped until frame: {level.frame}")
        plant = level.plant_data[chosen_action[0]].plant_name
        step += 1
        simulations = 10000
        print(f"Step {step} chosen actions {plant} at {chosen_action[1]}, {chosen_action[2]}")
        print("---------")
        print(f"Wins before: {level.rollout(8, simulations)} / {simulations}")
        level.step(cpp_level.Action(*chosen_action))
        print(f"Wins after: {level.rollout(8, simulations)} / {simulations}")
        print("=============================================")
    print(f"Victory: {level.win}")
    print(actions_taken)
    utils.simulate_set_game(backup_level, actions_taken)
        
    # test_level = cpp_level.Level(lanes, cols, 10, utils.lvl4_data, utils.chosen_plants_lvl4)
    # print(test_level.rollout(8, 10000))
    # action = cpp_level.Action(*chosen_action)
    # while not test_level.is_action_legal(action):
    #     test_level.step()
    # test_level.step(cpp_level.Action(*chosen_action))
    # print(test_level.rollout(8, 10000))
"""
steps:
1. choose a node according to UCB
2. Expand node using a list of random (legal) actions
3. rollout expanded nodes
4. update self ucb using child wins, plays
"""