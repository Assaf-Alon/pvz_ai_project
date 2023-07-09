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


Node* select(Node* root, Level& cloned_level, heuristic_function* h_func) {
    max_depth = 1;
    if (root->available_actions.size() > 0){
        return root;
    }
    Node* current_node = root;
    while (true) {
        if (cloned_level.done){
            return current_node;
        }
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
            if (h_func != nullptr && score == best_score){ // if score is the same, try to compare using the heuristic
                Level* clone_best = cloned_level.clone(FORCE_DETERMINISTIC);
                clone_best->deferred_step(best_node->action);
                Level* clone_node = cloned_level.clone(FORCE_DETERMINISTIC);
                clone_node->deferred_step(node->action);
                if ((*h_func)(*clone_node) > (*h_func)(*clone_best)) {
                    best_node = node;
                }
                delete clone_best;
                delete clone_node;
            }
        }
        if (best_score < current_node->ucb() && current_node->available_actions.size() > 0){
            return current_node;
        }
        current_node = best_node;
        cloned_level.deferred_step(current_node->action);
        max_depth++;
    }
}
Node* expand(Node* selected_node, Level& cloned_level, heuristic_function* h_func) {
    if (cloned_level.done) {
        return selected_node;
    }
    if (selected_node->available_actions.size() == 0) {
        // std::cout << "this shouldnt happen!!!" << std::endl;
        // Its ok, we just selected a terminal node :)
        return selected_node;
    }
    int action_index = 0;
    if (h_func != nullptr){
        constexpr int sample_size = 5;
        int best_h = 0;
        int best_index = 0;
        for (int sample = 0; sample < sample_size; sample++){
            action_index = get_random_number(0, selected_node->available_actions.size() - 1);
            Action action = selected_node->available_actions[action_index];
            Level* sample_clone = cloned_level.clone(FORCE_DETERMINISTIC);
            sample_clone->deferred_step(action);
            double sample_h = (*h_func)(*sample_clone);
            if (sample_h > best_h){
                best_h = sample_h;
                best_index = action_index;
            }
        }
        action_index = best_index;
    }
    else {
        action_index = get_random_number(0, selected_node->available_actions.size() - 1);
    }
    Action chosen_action = selected_node->available_actions[action_index];
    Node* child = new Node(selected_node, chosen_action);
    selected_node->children.push_back(child);
    selected_node->available_actions.erase(selected_node->available_actions.begin() + action_index);
    return child;
}
void rollout(Node* selected_node, Level& cloned_level) {
    cloned_level.deferred_step(selected_node->action);
    switch (rollout_mode){
        case MAX_NODE: // parallelization with max
        {
            if (cloned_level.done){
                // selected_node->available_actions.clear();
                selected_node->wins = (int)cloned_level.win;
                selected_node->simulations = 1;
                return;
            }
            selected_node->wins = cloned_level.rollout(rollouts_per_leaf, 1) ? 1 : 0;
            selected_node->simulations = 1;
        }
        break;
        case AVG_NODE: // parallelization with avg
        {
            if (cloned_level.done){
                // selected_node->available_actions.clear();
                selected_node->wins = (int)cloned_level.win * rollouts_per_leaf;
                selected_node->simulations = rollouts_per_leaf;
                return;
            }
            selected_node->wins = cloned_level.rollout(rollouts_per_leaf, 1);
            selected_node->simulations = rollouts_per_leaf;
        }
        break;
        default: // no parallelization
        {
            if (cloned_level.done){
                // selected_node->available_actions.clear();
                selected_node->wins = (int)cloned_level.win;
                selected_node->simulations = 1;
                return;
            }
            selected_node->wins = cloned_level.rollout(1, 1);
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

double heuristic_basic_sunflowers(const Level& level)
{
    // float score = 0.05 * (std::min(5, level.count_plant(SUNFLOWER))) * (level.frame < 1000);
    return 0.05 * (std::min(5, level.count_plant(SUNFLOWER)));// * (level.frame < 1000);
}


Action run(Level& level, int timeout_ms, int simulations_per_leaf, bool debug, float ucb_const, int mode, int heurisic_mode){
    // Setup
    // omp_set_num_threads(8);
    if (action_space.size() == 0){
        action_space = vector<Action>(level.get_action_space());
        std::cout << "Action space size: " << action_space.size() << std::endl;
    }
    ucb_coefficient = ucb_const;
    rollouts_per_leaf = simulations_per_leaf;
    rollout_mode = mode;
    if (mode == PARALLEL_TREES){
        return _parallel_trees_run(level, timeout_ms, simulations_per_leaf, debug, heurisic_mode);
    }
    Node root(nullptr, Action());

    // Timing
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    int num_expanded_nodes = 0;

    // Heuristic functions
    heuristic_function* selection_heuristic = nullptr;
    heuristic_function* expansion_heuristic = nullptr;
    if (heurisic_mode == HEURISTIC_MCTS || heurisic_mode == HEURISTIC_SELECT){
        selection_heuristic = new heuristic_function(heuristic_basic_sunflowers);
    }
    if (heurisic_mode == HEURISTIC_MCTS || heurisic_mode == HEURISTIC_EXPAND){
        expansion_heuristic = new heuristic_function(heuristic_basic_sunflowers);
    }

    // Main loop
    while (std::chrono::high_resolution_clock::now() < end_time){
        Level* cloned_level = level.clone(FORCE_RANDOM); // "guess" for how the level is going to look
        Node* next_node = select(&root, *cloned_level, selection_heuristic); // select node in tree, doing actions along the way
        Node* new_node = expand(next_node, *cloned_level, expansion_heuristic); // create new child node for selected node
        rollout(new_node, *cloned_level); // simulate game from new node
        backpropagate(new_node); // backpropagate victories, simulations from new node
        num_expanded_nodes++;
        delete cloned_level;
    }
    Action chosen_action = select_best_action(root).first;
    if (debug) {
        std::cout << "total expanded: " << num_expanded_nodes << ", total winrate: " << root.wins << std::endl;
    }
    if (selection_heuristic != nullptr){
        delete selection_heuristic;
    }
    if (expansion_heuristic != nullptr){
        delete expansion_heuristic;
    }
    return chosen_action;
}
Action _parallel_trees_run(Level& level, int timeout_ms, int num_trees, bool debug, int heurisic_mode){
    omp_set_num_threads(8);
    // std::vector<Node*> roots;
    // for (int i = 0; i < num_trees; i++){
    //     roots.push_back(new Node(nullptr, Action()));
    // }
    std::vector<Node> roots = std::vector<Node>(num_trees, Node(nullptr, Action()));
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);

    heuristic_function* selection_heuristic = nullptr;
    heuristic_function* expansion_heuristic = nullptr;
    if (heurisic_mode == HEURISTIC_MCTS || heurisic_mode == HEURISTIC_SELECT){
        selection_heuristic = new heuristic_function(heuristic_basic_sunflowers);
    }
    if (heurisic_mode == HEURISTIC_MCTS || heurisic_mode == HEURISTIC_EXPAND){
        expansion_heuristic = new heuristic_function(heuristic_basic_sunflowers);
    }

    std::vector<int> num_expanded_nodes = std::vector<int>(num_trees, 0);
    #pragma omp parallel for shared(roots)
    for (int tree = 0; tree < num_trees; tree++){
        while (std::chrono::high_resolution_clock::now() < end_time) {
            Level* cloned_level = level.clone(FORCE_RANDOM);
            Node* next_node = select(&roots[tree], *cloned_level, selection_heuristic); // select node in tree, doing actions along the way
            Node* new_node = expand(next_node, *cloned_level, expansion_heuristic); // create new child node for selected node
            rollout(new_node, *cloned_level);
            backpropagate(new_node);
            num_expanded_nodes[tree]++;
        }
    }
    std::unordered_map<Action, int, ActionHash> visits; // for each action, how many times it was visited
    visits.reserve(action_space.size());
    for (int i = 0; i < num_trees; i++){        
        for (auto node: roots[i].children){
            if (visits.find(node->action) == visits.end()){
                visits[node->action] = node->simulations;
            }
            else {
                visits[node->action] += node->simulations;
            }
        }
    }
    if (debug) {
        int total_expanded = 0;
        int total_wins = 0;
        for (int tree = 0; tree < num_trees; tree++){
            std::cout << "tree " << tree << ": total expanded: " << num_expanded_nodes[tree] << ", total wins: " << roots[tree].wins << std::endl;
            total_expanded += num_expanded_nodes[tree];
            total_wins += roots[tree].wins;
        }
        std::cout << "total expanded nodes: " << total_expanded << ", total wins: " << total_wins << std::endl;
    }
    auto iter = std::max_element(visits.begin(), visits.end(), \
        [](const auto &action_pair_1, const auto &action_pair_2) { 
            return action_pair_1.second < action_pair_2.second;
    });
    if (selection_heuristic != nullptr){
        delete selection_heuristic;
    }
    if (expansion_heuristic != nullptr){
        delete expansion_heuristic;
    }
    return iter->first;
}