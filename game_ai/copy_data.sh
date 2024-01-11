#!/bin/bash
echo 'level,time_ms,threads,ucb_const,rollout_mode,heuristic_mode,selection_mode,loss_heuristic,win,num_steps' > results/all.csv
cat results/mcts_experiment* >> results/all.csv
mv results/all.csv data/data.csv
