# Plants vs. Zombies AI using MCTS

## Introduction
This project was created as a part of the course "Project in AI" in the Technion.  
The project focuses on implementing Monte Carlo Tree Search (MCTS) to play the game "Plants vs. Zombies" (PvZ).  
The codebase consists of a C++ implementations of PvZ and the core MCTS functions (select, expand, rollout, backpropagate).  
For enhanced accessibility and ease of use, the above implementation can be converted to a Python package using Swig.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

### Prerequisites

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

3. Update the `LD_LIBRARY_PATH` environment variable and start running simulations
```bash
    export LD_LIBRARY_PATH=$(realpath ./build):$LD_LIBRARY_PATH
    python3 mcts.py
```

## Usage
TODO