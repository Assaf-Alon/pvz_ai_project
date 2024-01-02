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
- [Usage](#usage)

## Installation

### Prerequisites

0. Ubuntu Linux / WSL with Python3.11 installed

1. Install relevant dependencies:
```bash
    apt-get update
    apt-get install -y libpython3-dev
    apt-get install -y bash wget nano curl make libgmp3-dev libomp-dev tree swig
    apt-get install -y clang-format clang-tidy clang-tools clang clangd libc++-dev libc++1 libc++abi-dev libc++abi1 libclang-dev libclang1 liblldb-dev libllvm-ocaml-dev libomp-dev libomp5 lld lldb llvm-dev llvm-runtime llvm python3-clang
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

> **_NOTE:_**  If you get the following error: `fatal error: 'Python.h' file not found`, try to install python3.11-dev by running `sudo apt-get install python3.11-dev`.

3. Update the `LD_LIBRARY_PATH` environment variable and start running simulations
```bash
    export LD_LIBRARY_PATH=$(realpath ./build):$LD_LIBRARY_PATH
    python3 mcts.py
```

## CPP Environment
The C++ environment reveals an interface needed for the MCTS to run, but isn't limited to MCTS.
You can use the C++ environment to play a game manually, from C++ if you choose to.
> **_NOTE:_**  We worked really hard to enable using this library in Python. Instructions can be found below

An example
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
TODO

## Usage
TODO

## Run in a Container
In the root directory there are two [singularity](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html) definition files that define container images.
> [!NOTE]  
> Docker can work just fine as well. The main reason we're using Singularity is because we don't have root permission on the runtime environment.

### base_img.def
Uses the image `python:3.11.4-slim-bookworm` as a base image (baseception?).
Installs on top of it the relevant dependencies so we won't have to install them on each new build.

### pvz.def
Uses the image `base_img.sif` (built from base_img.def) as a base image.
copies the source files to the image, compiles and configure environment.
On runtime, runs the `mcts.py` script.
