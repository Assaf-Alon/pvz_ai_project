# Build Singularity image
sudo singularity build base_img.sif base_img.def
sudo singularity build pvz.sif pvz.def

# TODO:

## Interesting:
1. Implement Simulated annealing to create level data with specific random victory chance
    1. Add python proxy object for c++ level_data
    2. Add get_neighbour() function that finds a random neighbour of current level_data
    3. Add transition function
    4. Define restart policy
    5. Define temp cooldown policy
2. Implement MCTS to win actual games
    1. Choose selection, expension policies
    2. Level copy vs action in each node
    3. Compare tradeoff of accuracy vs speed (lots of low acc rollouts vs less high acc rollouts)
    4. Paper questions:
        1. Approaches to calculate relative value of multiple-rollout leaves: max/mean/avg/no normalization (naive)
            https://arxiv.org/pdf/2003.13741.pdf
            https://dke.maastrichtuniversity.nl/m.winands/documents/multithreadedMCTS2.pdf
            https://link.springer.com/article/10.1007/s10462-022-10228-y
        2. Changes to UCB to account for multiple rollouts
        3. C value 
        4. leaf parallelization vs root parallelization
3. Impement RL, compare to MCTS
    1. high-info large state vs low-info small state
    2. GPU acceleration


## Not Interesting:
0. Add "num_available_actions" to c++
1. Add state output to c++ (add selector for generating or not generating state)
2. Finish implementing plants in c++
3. Add option to clone with different FPS value
4. Add module to print result graphs (for Shaul)
5. Make sure plants work correctly, unit tests
6. Add user-readable print/render to level
7. Clean up c++ files (private/public, headers, game.hpp???)
8. makefile delta-based build
9. Documentation
10. Add another type of random action (choose next plant to plant, do it when possible isntead of choosing action that's legal now)
11. Skip actions for frames that have no legal actions
12. Add remove plant action at low probability
13. Night levels/ conveyor belt levels
14. Interface with pygame implementation?
15. Clean up repo even more

## Notes:
1. When dealing with RL, grid should look as follows:
arr(lanes, arr(cols, cell))
cell is an arr: plant_type, plant_hp, num_zombies, zombie_tier
zombie_tier is an int that is a function of:
    1. total hp of zombies in this cell (in hundreds? twenties?)
    2. avg move speed of zombies in this cell
