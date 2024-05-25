#!/bin/bash

rsync -rva dgershko@132.68.39.159:/home/dgershko/data/ new_Data/
echo 'level,time_ms,threads,ucb_const,rollout_mode,heuristic_mode,selection_mode,loss_heuristic,win,num_steps' > new_Data/all.csv
cat new_Data/mcts_*.csv >> new_Data/all.csv
mv new_Data/all.csv data/data.csv