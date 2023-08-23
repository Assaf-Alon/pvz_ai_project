#include "mcts.h"
#include <algorithm>
#include <unordered_map>
#include "../cpp_env/zombie.hpp"
#include "../cpp_env/plant.hpp"

#define LOSS_BOUND 0.1

int rollout_mode = NORMAL_MCTS;
float ucb_coefficient = 1.4;
int rollouts_per_leaf = 1;
int max_depth = 0;
int selection_mode = FULL_EXPAND;
heuristic_function h_func;
LossHeuristic *l_h_func;

inline void print_action(const Action& action, Level& level){
    std::cout << "chosen action: " << plant_data[action.plant_name].plant_name << " at " << action.lane << ", " << action.col;
}

// inline double decent_probability_threshold(int num_children) {
//     /*
//     Returns a number between 0 and 1. The threshold is exponential in the ratio between the number of children and the total number of actions.
//     */
//     double ratio = num_children / (float) action_space.size();
//     double threshold = pow(ratio, 4);
//     return threshold;
// }

std::pair<Action, int> select_best_action(Node& root) {
    Action action = Action();
    int most_rollouts = 0;
    int most_rollouts_wins = 0;
    // select the action of the most visited child. Use number of wins as a tie-breaker
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

Node* select(Node* root, Level& cloned_level, bool use_heuristic) {
    max_depth = 1;
    // if (selection_mode == ROOT_FULL_EXPAND && root->available_actions.size() > 0){
    //     return root;
    // }
    Node* current_node = root;
    while (true) {
        if (cloned_level.done){
            break;
        }
        else if (current_node->children.size() == 0){
            break;
        }
        if (current_node->available_actions.size() > 0) { // if there are still unexplored actions
            if (selection_mode == FULL_EXPAND){
                break;
            }
            else if (selection_mode == SQUARE_RATIO && get_random_float(0, 1) >= pow(current_node->children.size() / (float)action_space.size(), 2)){
                // as ratio approaches 1, chance of selecting self approaches 0
                break;
            }
            // else if (selection_mode == LINEAR_RATIO && get_random_float(0, 1) >= current_node->children.size() / (float)action_space.size()){
            //     // as ratio approaches 1, chance of selecting self approaches 0
            //     break;
            // }
        }
        float best_score = -1;
        Node* best_node = nullptr;
        for (auto node: current_node->children){
            float score = node->ucb();
            if (score > best_score){
                best_score = score;
                best_node = node;
            }
            if (use_heuristic && score == best_score){ // if score is the same, try to compare using the heuristic
                if (h_func(cloned_level, node->action) > h_func(cloned_level, best_node->action)) {
                    best_node = node;
                }
            }
        }
        if (best_score < current_node->ucb() && current_node->available_actions.size() > 0){
            break;
        }
        current_node = best_node;
        cloned_level.deferred_step(current_node->action);
        max_depth++;
    }
    // for (int i = 0; i < max_depth; i++){
    //     std::cout << "|--";
    // }
    // std::cout << "node: " << current_node->children.size() << " children";
    // std::cout << ", available actions: " << current_node->available_actions.size();
    // std::cout << ", depth: " << max_depth;
    // std::cout << ", simulations: " << current_node->simulations;
    // std::cout << ", wins: " << current_node->wins << std::endl;
    return current_node;
}
Node* expand(Node* selected_node, Level& cloned_level) {
    if (cloned_level.done) {
        return selected_node;
    }
    if (selected_node->available_actions.size() == 0) {
        // std::cout << "this shouldnt happen!!!" << std::endl;
        // Its ok, we just selected a terminal node :)
        return selected_node;
    }
    int action_index = 0;
    action_index = get_random_number(0, selected_node->available_actions.size() - 1);
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
                selected_node->wins = (int)cloned_level.win;
                selected_node->simulations = 1;
                return;
            }
            // There's at least one win <==> The result of the rollouts is greater than num_games * <heuristic bound>
            selected_node->wins = (int)(cloned_level.rollout(rollouts_per_leaf, 1, l_h_func) > rollouts_per_leaf * LOSS_BOUND);
            selected_node->simulations = 1;
        }
        break;
        case AVG_NODE: // parallelization with avg
        {
            if (cloned_level.done){
                selected_node->wins = (int)cloned_level.win * rollouts_per_leaf;
                selected_node->simulations = rollouts_per_leaf;
                return;
            }
            selected_node->wins = cloned_level.rollout(rollouts_per_leaf, 1, l_h_func);
            selected_node->simulations = rollouts_per_leaf;
        }
        break;
        default: // no parallelization
        {
            if (cloned_level.done){
                selected_node->wins = (int)cloned_level.win;
                selected_node->simulations = 1;
                return;
            }
            selected_node->wins = cloned_level.rollout(1, 1, l_h_func);
            selected_node->simulations = 1;
        }
        break;
    }
}
void backpropagate(Node* start_node) {
    int new_wins = start_node->wins;
    int new_simulations = start_node->simulations;
    if(start_node->parent == nullptr){
        return;
    }
    Node* current_node = start_node->parent;
    while (current_node != nullptr){
        current_node->wins += new_wins;
        current_node->simulations += new_simulations;
        current_node = current_node->parent;
    }
}

double heuristic_basic_sunflowers(const Level& level, const Action& action)
{
    /*
    Counts the number of sunflowers currently planted, adds 1 if the action is "plant sunflower" and returns min(5, num_sunflowers)
    */
    int num_sunflowers = level.count_plant(SUNFLOWER) + (action.plant_name == SUNFLOWER);
    return 0.05 * (std::min(5, num_sunflowers));
}

double loss_heurisitc_frame(const Level& level){ // loss heuristic 1
    return LOSS_BOUND * tanh(level.frame / 5000);
}
double loss_heurisitc_plant_cost(const Level& level){ // loss heuristic 2
    int plant_cost_sum = 0;
    for (const Plant* plant : level.plant_list){
        plant_cost_sum += plant->cost;
    }
    return LOSS_BOUND * tanh(plant_cost_sum / 1000);
}
double loss_heurisitc_zombies_on_board(const Level& level){ // loss heuristic 3
    int zombie_hp = 0;
    for (const Zombie* zombie : level.zombie_list){
        zombie_hp += zombie->hp;
    }
    return LOSS_BOUND * tanh(zombie_hp / 1000);
}
double loss_heuristic_zombies_left_to_spawn(const Level& level){ // loss heuristic 4
    return LOSS_BOUND * (1 - tanh((float)level.level_data.size() / 50));
}

Action run(Level& level, int timeout_ms, int simulations_per_leaf, bool debug, float ucb_const, int mode, int heuristic_mode, int selection_type, int loss_heuristic){
    // Setup
    omp_set_num_threads(NUM_CPU);
    if (action_space.size() == 0){
        action_space = vector<Action>(level.get_action_space());
        action_space_size = (int)action_space.size();
        std::cout << "Action space size: " << action_space_size << std::endl;
    }
    ucb_coefficient = ucb_const;
    rollouts_per_leaf = simulations_per_leaf;
    rollout_mode = mode;
    selection_mode = selection_type;
    switch (loss_heuristic)
    {
        case NO_HEURISTIC:
            l_h_func = nullptr;
        break;
        case FRAME_HEURISTIC:
            l_h_func = new LossHeuristic(loss_heurisitc_frame);
        break;
        case TOTAL_PLANT_COST_HEURISTIC:
            l_h_func = new LossHeuristic(loss_heurisitc_plant_cost);
        break;
        case TOTAL_ZOMBIE_HP_HEURISTIC:
            l_h_func = new LossHeuristic(loss_heurisitc_zombies_on_board);
        break;
        case ZOMBIES_LEFT_TO_SPAWN_HEURISTIC:
            l_h_func = new LossHeuristic(loss_heuristic_zombies_left_to_spawn);
        break;
    }
    int max_depth_reached = 0;
    if (mode == PARALLEL_TREES){
        return _parallel_trees_run(level, timeout_ms, simulations_per_leaf, debug, heuristic_mode);
    }
    Node root(nullptr, Action());

    // Timing
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    int num_expanded_nodes = 0;

    // Heuristic functions
    if (heuristic_mode != NO_HEURISTIC){
        h_func = heuristic_function(heuristic_basic_sunflowers);
    }
    bool heuristic_select = heuristic_mode == HEURISTIC_SELECT;
    // bool heuristic_expand = heuristic_mode == HEURISTIC_EXPAND || heuristic_mode == HEURISTIC_MCTS;

    // Main loop
    while (std::chrono::high_resolution_clock::now() < end_time){
        Level* cloned_level = level.clone(FORCE_RANDOM); // "guess" for how the level is going to look
        Node* next_node = select(&root, *cloned_level, heuristic_select); // select node in tree, doing actions along the way
        Node* new_node = expand(next_node, *cloned_level); // create new child node for selected node
        rollout(new_node, *cloned_level); // simulate game from new node
        backpropagate(new_node); // backpropagate victories, simulations from new node
        num_expanded_nodes++;
        delete cloned_level;
        if (debug){
            if (max_depth > max_depth_reached){
                max_depth_reached = max_depth;
            }
        }
    }
    Action chosen_action = select_best_action(root).first;
    if (debug) {
        std::cout << "total expanded: " << num_expanded_nodes << ", total winrate: " << root.wins;
        std::cout << ", root children expanded: " << root.children.size() << ", total simulations: " << root.simulations << " max depth reached: " << max_depth_reached << std::endl;
    }
    if (l_h_func != nullptr)
        delete l_h_func;
    return chosen_action;
}
Action _parallel_trees_run(Level& level, int timeout_ms, int num_trees, bool debug, int heuristic_mode){
    // Note: Parallel trees are not compatible with the expansion heuristic!
    // omp_set_num_threads(8);
    // std::vector<Node*> roots;
    // for (int i = 0; i < num_trees; i++){
    //     roots.push_back(new Node(nullptr, Action()));
    // }
    std::vector<Node> roots = std::vector<Node>(num_trees, Node(nullptr, Action()));
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);

    if (heuristic_mode != NO_HEURISTIC){
        h_func = heuristic_function(heuristic_basic_sunflowers);
    }
    bool heuristic_select = heuristic_mode == HEURISTIC_SELECT;

    std::vector<int> num_expanded_nodes = std::vector<int>(num_trees, 0);
    #pragma omp parallel for shared(roots)
    for (int tree = 0; tree < num_trees; tree++){
        while (std::chrono::high_resolution_clock::now() < end_time) {
            Level* cloned_level = level.clone(FORCE_RANDOM);
            Node* next_node = select(&roots[tree], *cloned_level, heuristic_select); // select node in tree, doing actions along the way
            Node* new_node = expand(next_node, *cloned_level); // create new child node for selected node
            rollout(new_node, *cloned_level); // simulate game from new node
            backpropagate(new_node); // backpropagate victories, simulations from new node
            num_expanded_nodes[tree]++;
            // for (int i = 0; i < EXPAND_BATCH; i++){ // expand multiple children at once
            //     Node* new_node = expand(next_node, *cloned_level); // create new child node for selected node
            //     rollout(new_node, *cloned_level); // simulate game from new node
            //     backpropagate(new_node); // backpropagate victories, simulations from new node
            //     num_expanded_nodes[tree]++;
            //     if (next_node->available_actions.size() == 0){
            //         break;
            //     }
            // }
            delete cloned_level;
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
            std::cout << "tree " << tree << ": total expanded: " << num_expanded_nodes[tree] << ", total wins: " << roots[tree].wins;
            std::cout << ", num root actions tried: " << roots[tree].children.size() << std::endl;
            total_expanded += num_expanded_nodes[tree];
            total_wins += roots[tree].wins;
        }
        std::cout << "total expanded nodes: " << total_expanded << ", total wins: " << total_wins << std::endl;
    }
    if (l_h_func != nullptr)
        delete l_h_func;
    auto iter = std::max_element(visits.begin(), visits.end(), \
        [](const std::pair<Action, int> &action_pair_1, const std::pair<Action, int> &action_pair_2) { 
            return action_pair_1.second < action_pair_2.second;
    });
    return iter->first;
}