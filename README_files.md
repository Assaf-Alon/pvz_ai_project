# README - Files Origin

As instructed, this file describes the files used in this project.
All these files were written by us.

- base_img.def - Defines the base container image with needed dependencies to compile and run simulations
- pvz.def - Defines final container, with built source code. Runs the simulations.
- game_ai
  - game_engine
    - level.cpp - Implementation of the Level class that manges the gameplay of a Plant vs. Zombies game.
    - level.hpp - Definition of the Level class and related classes and functions.
    - level.i - Defines Swig settings for the Level class and more.
    - plant.cpp - Implementation of the Plant class that represents a deployed plant.
    - plant.hpp - Definition of the Plant class.
    - zombie.cpp - Implementation of the Zombie class that represents a deployed zombie.
    - zombie.hpp - Definition of the Zombie class.

  - cpp_mcts
    - mcts.cpp - Implementation of the MCTS functions, such as expand and rollout.
    - mcts.h - Definition of the MCTS functions, along with the MCTS Node class and more.
    - mcts.i - Defines Swig settings for the MCTS functions.

  - data
    - levels.json - Defines the used levels - zombie type, lane, and spawn time.
    - all.csv - The results of all experiments done
    - cleaned.csv - Aggregated results with statistical data added
    - graph_params.csv - Subset of cleaned.csv which contains all the data used to generate the graphs
  
  - graphs
    - All graphs used in the project.

  - games.hpp - Declares and implements common functions for different games.
  - main.cpp - An example of a raw usage of the C++ library.
  - main.py - An example of running the game using the python bindings. Includes a graphical representation of the game
  - Makefile - Describes different compilation rules.
  - mcts_experiment.py - Runs the experiments by the defined parameters.
  - generate_game_animation.py - Generates an animation of a run of the game, saved to animation.mp4.
  - data_analysis.py - Aggregates the results of the experiments and generates the graphs.
  - test_full.py - Unit tests that verify the engine acts as intended.
  - utils.py - Common utilities to run simulations in Python.