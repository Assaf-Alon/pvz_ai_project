# Instructions to Reproduce Data
To recreate the experiments we ran, you should follow the instructions in the README.md to build the image with Singularity.
Before building the image pvz.sif, update the file `game_ai/mcts.py` and update the following lines:

```python
    time_range = [6400]  # List of numbers
    ucb_range = [0.0001, 0.0005, 0.001, 0.004, 0.006, 0.008, 0.016, 0.064, 0.256]  # List of numbers
    level_range = ["9+", "9++"]  # Must be a valid level from the game_ai/data/levels.json file
    expansion_modes = [mcts.NORMAL_MCTS, mcts.PARALLEL_TREES]  # Valid types: [mcts.NORMAL_MCTS, mcts.MAX_NODE, mcts.AVG_NODE, mcts.PARALLEL_TREES]
    heuristic_modes = [mcts.NO_HEURISTIC]  # Valid types: [mcts.NO_HEURISTIC, mcts.HEURISTIC_SELECT]
    selection_modes = [mcts.FULL_EXPAND,]  # Valid types: [mcts.FULL_EXPAND, mcts.SQUARE_RATIO]
    loss_heuristic = [mcts.NO_HEURISTIC]  # Valid types: [mcts.NO_HEURISTIC, mcts.FRAME_HEURISTIC mcts.TOTAL_PLANT_COST_HEURISTIC, mcts.TOTAL_ZOMBIE_HP_HEURISTIC, mcts.ZOMBIES_LEFT_TO_SPAWN_HEURISTIC]
    threads = [8]  # List of integers, up to the amount of threads available
    experiment_parameter_list = list(itertools.product(\
        level_range, time_range, threads, ucb_range, expansion_modes, heuristic_modes, selection_modes, loss_heuristic
    ))

```
The experiments that will be ran are all combinations of parameters given.
For example, the above will run for 6.4 seconds, experiments with ALL the given UCB values, on both level 9+ and 9++.
If you want to test a specific parameter (In the above example, UCB), it is recommended not to add too many different values to other parameters, as it might increase the runtime exponentially.