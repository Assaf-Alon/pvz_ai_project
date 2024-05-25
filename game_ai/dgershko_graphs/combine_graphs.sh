#!/bin/zsh

convert +append *core*.png threads.png # combine thread graphs side by side
convert +append rollout_strategies_on* rollout_strategies.png # combine rollout strategies graphs side by side
convert +append heuristics_on_level_9+_-_normal_agent.png heuristics_on_level_9++_-_normal_agent.png  basic_heuristics.png # combine basic heuristics graphs side by side
convert +append loss_heuristic_on_level_9+_-_normal_agent.png loss_heuristic_on_level_9++_-_normal_agent.png loss_heuristics.png # combine loss heuristics graphs side by side
convert +append selection_heuristic_on_level_9+.png selection_heuristic_on_level_9++.png selection_heuristics.png # combine selection heuristics graphs side by side