#!/bin/bash
rsync -rva dgershko@132.68.39.159:/home/dgershko/data/ results/
echo 'level,time_ms,threads,ucb_const,rollout_mode,heuristic_mode,win,num_steps' > results/all.csv
cat results/mcts_experiment* >> results/all.csv
mv results/all.csv data/data.csv
