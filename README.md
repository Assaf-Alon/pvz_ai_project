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
3. Impement RL, compare to MCTS
    1. high-info large state vs low-info small state
    2. GPU acceleration


## Not Interesting:
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