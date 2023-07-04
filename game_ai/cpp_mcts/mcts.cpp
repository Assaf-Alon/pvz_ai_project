#include "mcts.h"
#include <algorithm>
#include <unordered_map>

int rollout_mode = NORMAL_MCTS;
float ucb_coefficient = 1.4;
int rollouts_per_leaf = 1;
int max_depth = 0;

inline void print_action(const Action& action, Level& level){
    std::cout << "chosen action: " << plant_data[action.plant_name].plant_name << " at " << action.lane << ", " << action.col;
}

Node* expand(Node* selected_node) {
    if (selected_node->level->done) {
        return selected_node;
    }
    if (selected_node->available_actions.size() == 0) {
        std::cout << "this shouldnt happen!!!" << std::endl;
        return selected_node;
    }
    int action_index = get_random_number(0, selected_node->available_actions.size() - 1);
    Action chosen_action = selected_node->available_actions[action_index];
    Node* child = new Node(selected_node, *selected_node->level, chosen_action);
    selected_node->children.push_back(child);
    selected_node->available_actions.erase(selected_node->available_actions.begin() + action_index);
    return child;
}
void rollout(Node* selected_node) {
    selected_node->level->deferred_step(selected_node->action);
    switch (rollout_mode){
        case MAX_NODE: // parallelization with max
        {
            if (selected_node->level->done){
                selected_node->available_actions.clear();
                selected_node->wins = (int)selected_node->level->win;
                selected_node->simulations = 1;
                return;
            }
            selected_node->wins = selected_node->level->rollout(rollouts_per_leaf, 1) ? 1 : 0;
            selected_node->simulations = 1;
        }
        break;
        case AVG_NODE: // parallelization with avg
        {
            if (selected_node->level->done){
                selected_node->available_actions.clear();
                selected_node->wins = (int)selected_node->level->win * rollouts_per_leaf;
                selected_node->simulations = rollouts_per_leaf;
                return;
            }
            selected_node->wins = selected_node->level->rollout(rollouts_per_leaf, 1);
            selected_node->simulations = rollouts_per_leaf;
        }
        break;
        default: // no parallelization
        {
            if (selected_node->level->done){
                selected_node->available_actions.clear();
                selected_node->wins = (int)selected_node->level->win;
                selected_node->simulations = 1;
                return;
            }
            selected_node->wins = selected_node->level->rollout(1, 1);
            selected_node->simulations = 1;
        }
        break;
    }
}
void backpropagate(Node* start_node) {
    int new_wins = start_node->wins;
    int new_simulations = start_node->simulations;
    Node* current_node = start_node;
    while (current_node != nullptr){
        current_node->wins += new_wins;
        current_node->simulations += new_simulations;
        current_node = current_node->parent;
    }
}

Node* select(Node* root){
    max_depth = 1;
    if (root->available_actions.size() > 0){
        return root;
    }
    Node* current_node = root;
    while (true) {
        if (current_node->level->done){
            return current_node;
        }
        // if (current_node->available_actions.size() > 0){
        //     return current_node;
        // }
        if (current_node->children.size() == 0){
            return current_node;
        }
        float best_score = -1;
        Node* best_node = nullptr;
        for (auto node: current_node->children){
            float score = node->ucb();
            if (score > best_score){
                best_score = score;
                best_node = node;
            }
        }
        if (best_score < current_node->ucb() && current_node->available_actions.size() > 0){
            return current_node;
        }
        current_node = best_node;
        max_depth++;
    }
}

Node* select(Node* root, heuristic_function func){
    max_depth = 1;
    if (root->available_actions.size() > 0){
        return root;
    }
    Node* current_node = root;
    while (true) {
        if (current_node->level->done){
            return current_node;
        }
        // if (current_node->available_actions.size() > 0){
        //     return current_node;
        // }
        if (current_node->children.size() == 0){
            return current_node;
        }
        float best_score = -1;
        Node* best_node = nullptr;
        for (auto node: current_node->children){
            float score = node->ucb() + func(*(node->level));
            if (score > best_score){
                best_score = score;
                best_node = node;
            }
        }
        if (best_score < current_node->ucb() + func(*(current_node->level)) && current_node->available_actions.size() > 0){
            return current_node;
        }
        current_node = best_node;
        max_depth++;
    }
}

std::pair<Action, int> select_best_action(Node& root) {
    Action action = Action();
    int most_rollouts = 0;
    int most_rollouts_wins = 0;
    for (auto node: root.children) {
        // std::cout << "ucb value: " << node->ucb() << ", wins: " << node->wins << ", rollouts: " << node->simulations << std::endl;
        if (node->simulations == most_rollouts && node->wins > most_rollouts_wins) {
            action = node->action;
            most_rollouts_wins = node->wins;
        }
        else if (node->simulations > most_rollouts) {
            most_rollouts_wins = node->wins;
            most_rollouts = node->simulations;
            action = node->action;
        }
    }
    return std::pair<Action, int>(action, most_rollouts);
}
Action run(Level& level, int timeout_ms, int simulations_per_leaf, bool debug, float ucb_const, int mode){
    if (rollouts_per_leaf > 1){
        omp_set_num_threads(8);
    }
    ucb_coefficient = ucb_const;
    rollouts_per_leaf = simulations_per_leaf;
    rollout_mode = mode;
    if (action_space.size() == 0){
        action_space = vector<Action>(level.get_action_space());
        std::cout << "Action space size: " << action_space.size() << std::endl;
    }
    if (rollout_mode == PARALLEL_TREES){
        return parralel_run(level, timeout_ms, simulations_per_leaf, debug, ucb_const);
    }
    Node* root = new Node(nullptr, level, Action());
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    int num_expanded_nodes = 0;
    int maximum_total_depth = 0;
    while(std::chrono::high_resolution_clock::now() < end_time && num_expanded_nodes < 800000) {
        Node* next_node;
        if (rollout_mode == HEURISTIC_MCTS) {
            next_node = select(root, heuristic_basic_sunflowers);
        }
        else {
            next_node = select(root);
        }
        if (max_depth > maximum_total_depth){
            maximum_total_depth = max_depth;
        }
        Node* new_node = expand(next_node);
        rollout(new_node);
        backpropagate(new_node);
        num_expanded_nodes++;
    }
    Action chosen_action = select_best_action(*root).first;
    if (debug) {
        std::cout << "total expanded: " << num_expanded_nodes << ", total winrate: " << root->wins << ", max depth achieved: " << maximum_total_depth << std::endl;
    }
    delete root;
    return chosen_action;
}
Action parralel_run(Level& level, int timeout_ms, int parralel_factor, bool debug, float ucb_const){
    vector<Node*> roots;
    for (int i = 0; i < parralel_factor; i++){
        roots.push_back(new Node(nullptr, level, Action()));
    }
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    omp_set_num_threads(8);
    #pragma omp parallel for shared(roots)
    for (int i = 0; i < parralel_factor; i++){
        while(std::chrono::high_resolution_clock::now() < end_time && roots[i]->simulations < 200000) {
            Node* next_node = select(roots[i]);
            Node* new_node = expand(next_node);
            rollout(new_node);
            backpropagate(new_node);
        }
    }
    Action chosen_action = Action();
    std::unordered_map<Action, int, ActionHash> visits; // for each action, how many times it was visited
    for (int i = 0; i < parralel_factor; i++){
        for (auto node: roots[i]->children){
            if (visits.find(node->action) == visits.end()){
                visits[node->action] = node->simulations;
            }
            else {
                visits[node->action] += node->simulations;
            }
        }
    }
    int most_visits = 0;
    for (const std::pair<Action, int> action_visits : visits){
        if (debug){
            print_action(action_visits.first, level);
            std::cout << ", visits: " << action_visits.second << std::endl;
        }
        if (action_visits.second > most_visits){
            most_visits = action_visits.second;
            chosen_action = action_visits.first;
        }
    }
    if (debug) {
        int total_rollouts = 0;
        for (int i = 0; i < parralel_factor; i++){
            total_rollouts += roots[i]->simulations;
        }
        std::cout << "total rollouts: " << total_rollouts << std::endl;
        std::cout << "Action chosen: ";
        print_action(chosen_action, level);
        std::cout << std::endl;
    }
    for (int i = 0; i < parralel_factor; i++){
        delete roots[i];
    }
    return chosen_action;
}
