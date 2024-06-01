#!/bin/bash
echo 'level,time_ms,threads,ucb_const,rollout_mode,heuristic_mode,selection_mode,loss_heuristic,win,num_steps' > all.csv
cat final_csv/mcts_experiment* >> all.csv
