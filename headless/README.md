## Objectives:

1. Write an analogue of the normal PVZ game that's as close as possible to the original
2. Make the analogue run without GUI for running in the cloud
3. Make the analogue as fast as possible to speed up rollouts/learning
4. Create a translation layer between the normal GUI game and this analogue

## TODOs:

1. Explore switching lists to dicts for easy deletion of killed objects
2. Implement all Plant types
3. Implement all zombie types (check if subclassing is necessary)
4. Implement an fps switch (delays between actions are in frames, adjust accordingly)
5. Implement level randomization
6. Implement state output
7. Implement user action (be careful with illegal operators)
8. (?) Add GUI mode
9. Make JSON reading happen once on import instead of each time an object is created (I/O overhead)
10. Change zombie spawning mechanism (List instead of dict)
10.1. Implement victory (no more zombies to spawn, no more zombies on the map)