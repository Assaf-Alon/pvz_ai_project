#include "mcts.h"

// int rollout_mode = 0;
float ucb_coefficient = 1.4;
int rollouts_per_leaf = 1;

inline void print_action(Action& action, Level& level){
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
void rollout(Node* selected_node, int rollout_mode) {
    selected_node->level->deferred_step(selected_node->action);
    switch (rollout_mode){
        case 0: // no parallelization
            if (selected_node->level->done){
                selected_node->available_actions.clear();
                selected_node->wins = (int)selected_node->level->win;
                selected_node->simulations = 1;
                return;
            }
            selected_node->wins = selected_node->level->rollout(1, 1, 1);
            selected_node->simulations = 1;
        break;
        case 1: // parallelization with max 
            if (selected_node->level->done){
                selected_node->available_actions.clear();
                selected_node->wins = (int)selected_node->level->win;
                selected_node->simulations = 1;
                return;
            }
            selected_node->wins = selected_node->level->rollout(8, rollouts_per_leaf, 1) ? 1 : 0;
            selected_node->simulations = 1;
        break;
        case 2: // parallelization with avg
            if (selected_node->level->done){
                selected_node->available_actions.clear();
                selected_node->wins = (int)selected_node->level->win * rollouts_per_leaf;
                selected_node->simulations = rollouts_per_leaf;
                return;
            }
            selected_node->wins = selected_node->level->rollout(8, rollouts_per_leaf, 1);
            selected_node->simulations = rollouts_per_leaf;
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

Node* select(Node* root, int rollout_mode){
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
            float score = node->ucb(rollout_mode);
            if (score > best_score){
                best_score = score;
                best_node = node;
            }
        }
        if (best_score < current_node->ucb(rollout_mode) && current_node->available_actions.size() > 0){
            return current_node;
        }
        current_node = best_node;
    }
}

std::pair<Action, int> select_best_action(Node& root) {
    Action action = Action();
    int most_rollouts = 0;
    int most_rollouts_wins = 0;
    for (auto node: root.children) {
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
Action run(Level& level, int timeout_ms, int games_per_rollout, bool debug, float ucb_const, int rollout_mode){
    ucb_coefficient = ucb_const;
    rollouts_per_leaf = games_per_rollout;
    if (action_space.size() == 0){
        action_space = vector<Action>(level.get_action_space());
    }
    if (rollout_mode == 3){
        return parralel_run(level, timeout_ms, games_per_rollout, debug, ucb_const);
    }
    Node* root = new Node(nullptr, level, Action());
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    int num_expanded_nodes = 0;
    while(std::chrono::high_resolution_clock::now() < end_time && root->simulations < 800000) {
        Node* next_node = select(root, rollout_mode);
        Node* new_node = expand(next_node);
        rollout(new_node, rollout_mode);
        backpropagate(new_node);
        num_expanded_nodes++;
    }
    Action chosen_action = select_best_action(*root).first;
    if (debug) {
        std::cout << "num of expanded nodes in tree: " << num_expanded_nodes << std::endl;
        std::cout << "total expanded: " << root->simulations << " total winrate: " << root->wins << std::endl;
    }
    delete root;
    return chosen_action;
}
Action parralel_run(Level& level, int timeout_ms, int parralel_factor, bool debug, float ucb_const){
    vector<Node*> roots = vector<Node*>();
    for (int i = 0; i < parralel_factor; i++){
        roots.push_back(new Node(nullptr, level, Action()));
    }
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    omp_set_num_threads(parralel_factor);
    #pragma omp parallel for shared(roots)
    for (int i = 0; i < parralel_factor; i++){
        while(std::chrono::high_resolution_clock::now() < end_time && roots[i]->simulations < 200000) {
            Node* next_node = select(roots[i], 0);
            Node* new_node = expand(next_node);
            rollout(new_node, 0);
            backpropagate(new_node);
        }
    }
    // vector<Action> chosen_actions = vector<Action>();
    Action chosen_action = Action();
    int most_rollouts = 0;
    for (int i = 0; i < parralel_factor; i++){
        std::pair<Action, int> action_with_rollouts = select_best_action(*roots[i]);
        if (action_with_rollouts.second > most_rollouts){
            most_rollouts = action_with_rollouts.second;
            chosen_action = action_with_rollouts.first;
        }
        if (debug) {
            std::cout << "total expanded: " << roots[i]->simulations << " total winrate: " << roots[i]->wins << std::endl;
            std::cout << "action chosen by tree: ";
            print_action(action_with_rollouts.first, *roots[i]->level);
            std::cout << " rollouts: " << action_with_rollouts.second << std::endl;
        }
        delete roots[i];
    }
    return chosen_action;
}
int heuristic1(const Level& level)
{
    return (10 * level.count_plant(SUNFLOWER) + 5 * level.count_lawnmowers()) * level.frame;
}

int heuristic2(const Level& level)
{
    return (5 * level.count_plant(SUNFLOWER) + 4 * level.count_lawnmowers() + 2 * level.count_plant()) * level.frame;
}