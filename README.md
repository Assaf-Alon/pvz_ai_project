# Plants vs. Zombies AI using MCTS

## Introduction
This project was created as a part of the course "Project in AI" in the Technion.  
The project focuses on implementing Monte Carlo Tree Search (MCTS) to play the game "Plants vs. Zombies" (PvZ).  
The codebase consists of a C++ implementations of PvZ and the core MCTS functions (select, expand, rollout, backpropagate).  
For enhanced accessibility and ease of use, the above implementation can be converted to a Python package using Swig.


## Table of Contents

- [Installation](#installation)
- [C++ Environment](#cpp-environment)
- [Python Environment](#python-environment)
- [MCTS](#monte-carlo-tree-search)
- [Run in a Container](#run-in-a-container)

## Installation

### Prerequisites

0. Ubuntu Linux / WSL with Python3.11 installed

1. Install relevant dependencies:
```bash
    sudo apt-get update
    sudo apt-get install -y libpython3-dev
    sudo apt-get install -y bash wget nano curl make libgmp3-dev libomp-dev tree swig
    sudo apt-get install -y clang-format clang-tidy clang-tools clang clangd libc++-dev libc++1 libc++abi-dev libc++abi1 libclang-dev libclang1 liblldb-dev libllvm-ocaml-dev libomp-dev libomp5 lld lldb llvm-dev llvm-runtime llvm python3-clang
```

2. Install Python packages:
```bash
    pip install numpy pandas matplotlib scipy
```

### Clone and Build

1. Clone the repository to your local machine:

```bash
    git clone https://github.com/Assaf-Alon/pvz_ai_project.git
```

2. Navigate to the project directory and build the project:
```bash
    cd pvz_ai_project/game_ai
    make clean && make -j8
```

> [!NOTE]  
> If you get the following error: `fatal error: 'Python.h' file not found`, try to install python3.11-dev by running `sudo apt-get install python3.11-dev`.

3. Update the `LD_LIBRARY_PATH` environment variable and start running simulations
```bash
    export LD_LIBRARY_PATH=$(realpath ./build):$LD_LIBRARY_PATH
    python3 mcts.py
```

## CPP Environment
The C++ environment reveals an interface needed for the MCTS to run, but isn't limited to MCTS.
You can use the C++ environment to play a game manually, from C++ if you choose to.
> [!NOTE]
> We worked really hard to enable using this library in Python. Instructions can be found below

An example code snippet:  
```cpp
#include level.hpp

bool play_easy_game() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate(15, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(60, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(95, 1, "normal"));
    std::vector<int> chosen_plants       = { SUNFLOWER, CHOMPER, PEASHOOTER, POTATOMINE };
    Action no_action = Action(NO_PLANT, 0,  0);

    //                lanes, columns, fps, level_data
    Level env = Level(5,     10,      10,  level_data, chosen_plants);
    while (!env.done) {
        Action next_action = ...; // Choose action, maybe by input from user
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
        }
        else {
            env.step(no_action);
        }
    }
    return env.win;
}
```

## Python Environment
The following are examples used in the code that utilize the built library.
### Creating level data from a list, play that level with random actions
```python
    from build import level

    def construct_level_data_from_list(list: list):
        list.sort(key=lambda item: item[0]) # sort by first element of tuple (list[tuple])
        level_data = level.ZombieQueue()
        for item in list:
            level_data.push_back(level.ZombieSpawnTemplate(item[0], item[1], item[2]))
        return level_data

    def get_level_info(level_num: int):
        with open("data/levels.json", "r") as level_json:
            levels = json.load(level_json)
        level_info = levels[f"level_{level_num}"]
        zombie_list, plant_list = level_info["zombies"], level_info["plants"]
        return construct_level_data_from_list(zombie_list), plant_list

    def play_level(level_num: int):
        FPS = 10
        GAMES = 10000
        env = level.Level(1, 10, FPS, *get_level_info(level_num))
        print(f"Level {level_num} Mode 1: {env.rollout(8, GAMES, 1)} / {GAMES}")
        print(f"Level {level_num} Mode 2: {env.rollout(8, GAMES, 2)} / {GAMES}")
        print(f"Level {level_num} Mode 3: {env.rollout(8, GAMES, 3)} / {GAMES}")
    
    play_level(1)
    play_level(2)
    play_level(3)
```

## Monte Carlo Tree Search
Similar to the `level` package built from the cpp code, a package called `mcts` was built as well.  
The file [mcts.py](/game_ai/mcts.py) is a great reference to understand how to use the package.  
Specifically the `perform_experiment` function might prove useful.  
A partial snippet from the file:
```python
    level_data, plant_list = utils.get_level_info(num_level)
    env = level.Level(5, 10, 10, level_data, plant_list, False)
    action_list = []
    while not env.done:
        action = mcts.run(env, int(time_ms), int(parallel_factor), False, float(ucb_const), int(rollout_mode), int(heuristic_mode), int(selection_mode), int(loss_heuristic))
        env.deferred_step(action)
        action_list.append(action)
        print(f"[{env.frame}] Action chosen: lane: {action.lane}, col: {action.col}, plant: {utils.plant_to_name[action.plant_name]}")
```

## Run in a Container
Running in a container can be useful to run MCTS experiments on a dedicated server without needing to install any of the required dependencies.  
In the root directory there are two [singularity](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html) definition files that define container images.
> [!NOTE]  
> Docker can work just fine as well. The main reason we're using Singularity is because we don't have root permission on the runtime environment.

### base_img.def
Uses the image `python:3.11.4-slim-bookworm` as a base image (baseception?).  
Installs on top of it the relevant dependencies so we won't have to install them on each new build.  
To build the image from the definition file run:
```bash
    sudo singularity build base_img.sif base_img.def
```

### pvz.def
Uses the image `base_img.sif` (built from base_img.def) as a base image.  
copies the source files to the image, compiles and configure environment.  
On runtime, runs the `mcts.py` script.  
To build the image from the definition file run:
```bash
    sudo singularity build pvz.sif pvz.def
```

### Run Container
To run the singularity container, run the following in the project root directory:
```bash
    singularity run --bind data:/home/game_ai/test_data pvz.sif
```
The above runs the image, mounting the local path `./data` to the path in the image: `/home/game_ai_test_data`.
