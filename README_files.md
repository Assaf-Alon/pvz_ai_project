# README - Files Origin

As instructed, this file describes the files used in this project.
All these files were written by us.

- base_img.def - Defines the base container image with needed dependencies to compile and run simulations
- pvz.def - Defines final container, with built source code. Runs the simulations.
- game_ai
  - cpp_env
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

  - games.hpp - Declares and implements common functions for different games.
  - main.cpp - An example of a raw usage of the C++ library.
  - Makefile - Describes different compilation rules.
  - mcts.py - Runs the experiments by the defined parameters.
  - test_full.py - Unit tests that verify the engine acts as intended.
  - utils.py - Common utilities to run simulations in Python.