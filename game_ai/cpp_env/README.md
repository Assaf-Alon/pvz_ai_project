# C++ Environment
C++ file related to "Plants vs. Zombies" engine.

# Files Description

The C++ engine's main components are:
- [The Plants](#plant-module)
- [The Zombies](#zombie-module)
- [The Level](#level-module)

## Plant Module
The plant module defines a Plant class, which contains all properties and methods related to a deployed plant.

### Notable Properties
- `lane` - The lane (y axis) in which the plant is located at.
- `col` - The column (x axis) in which the plant is located at.
- `hp` - The remaining health points the plant currently has.
- `action` - The action the plant performs.

> [!NOTE]
> The action property is a pointer to a function. A more Object-Oriented approach was attempted, but it severely hurt performance, so we decided to choose this approach instead.

### Notable Methods
- `do_action` - Performs the action stored in the `action` property if applicable.
- `get_damaged` - Damages the plant, reducing its health points. If killed, removes the plant from the board.


## Zombie Module
The zombie module defines a Zombie class, which contains all properties and methods related to an approaching zombie.

### Notable Properties
- `lane` - The lane in which the zombie is located in.
- `col` - The column in which the zombie is located in.
- `hp` - The remaining health points the zombie currently has.
- `move_interval_seconds` - The amount of seconds it takes for a zombie to move to the next tile.

### Notable Methods
- `attack` - Attacks the nearest plant.
- `move` - Move a tile closer to the player's base.
- `do_action` - Performs the action the zombie should do in a specific instance. This can be `attack`, `move`, or other possible custom actions for special zombies.


## Level Module
The level module contains the main code to manage the gameplay of a level.

### Notable Classes
- `Level` - Manages the gameplay of a certain level. Contains the current deployed plants and zombies, and invokes their actions as the game progresses. Notable properties and methods:
    - `lanes` - Property. The amount of lanes the level has.
    - `suns` - Property. The amount of suns (currency) currently in the player's possession.
    - `spawn_zombies` - Method. Spawns zombies if need be.
    - `do_player_action` - Method. Adds the plant the player has planted if need be.
    - `step` - Method. Moves 1 frame forward, performing any actions needed (like spawning zombies, performing the player's action, etc).

- `ZombieSpawnTemplate` - A collection of these defines how a level will play out, regarding spawned zombies. Contains the frame in which a zombie is spawned, the zombie type and its lane.
- `PlantData` - Contains constant data related to plants, like their price, initial hp, etc.



# Usage
TODO - update this

To compile:
make fast        // Basic
make debug       // Debug mode, extra prints
make clang-debug // Debug mode, extra prints, sanitizer
make fast-sanitize // sanitizer but without debug prints and with extra flags to find rare exceptions
(Then run `./main.out`)
make profile     // Uses gprof to profile the program
`./main.out`
`gprof main.out gmon.out > analysis.txt`

# clang-profile-optimize:
For optimal performance, run `make clang-profile-optimize`.
Note: this will take a while (30-100 sec), but generate code that is up to 2x faster.
