#include "mcts.h"

int rollout_mode = 0;
float ucb_coefficient = 1.4;
int rollouts_per_leaf = 1;

inline void print_action(Action& action, Level& level){
    std::cout << "chosen action: " << plant_data[action.plant_name].plant_name << " at " << action.lane << ", " << action.col << std::endl;
    
}

/*
Node* Node::select_with_heuristic() {
        if (this->children.size() == 0) {
        return this;
    }
    float best_ucb = 0;
    float ucb;
    Node* best_node = this->children[0];
    for (auto child : this->children) {
        ucb = child->ucb() + heuristic2(this->level);
        if (ucb > best_ucb) {
            best_ucb = ucb;
            best_node = child;
        }
    }
    // Children suck, should expand this node instead
    if (best_ucb < this->ucb() && this->available_actions.size() > 0){
        return this;
    }
    // All games are done
    if (best_node == nullptr) {
        return nullptr;
    }
    best_node = best_node->select_with_heuristic(); // recursive select node
    
    // Child leads to finished game, there're still actions to expand here
    if (best_node == nullptr && this->available_actions.size() > 0){
        return this;
    }
    return best_node;
} */

void Node::expand() {
    if (this->level->done) {
        return;
    }
    if (this->available_actions.size() == 0) {
        std::cout << "wtf" << std::endl;
        exit(0);
    }
    if (this->parent == nullptr) { // root node gets fully expanded 
        this->children.reserve(this->available_actions.size());
        for (auto action : this->available_actions) {
            Node* child = new Node(this, *this->level, action);
            child->rollout();
            // #pragma omp critical
            {
                this->children.push_back(child);
            }
        }
        this->available_actions.clear();
        return;
    }
    int action_index = get_random_number(0, this->available_actions.size() - 1);
    Action chosen_action = this->available_actions[action_index];
    Node* child = new Node(this, *this->level, chosen_action);
    child->rollout();
    this->children.push_back(child);
    this->available_actions.erase(this->available_actions.begin() + action_index);

}
void Node::rollout() {
    this->level->deferred_step(this->action);
    int wins = 0;
    int simulations = 1;
    switch (rollout_mode){
        case 0: // no parallelization
        if (this->level->done){
            this->backpropagate((int)this->level->win, 1);
            this->available_actions.clear();
            return;
        }
        wins = this->level->rollout(1, 1, 1);
        break;
        case 1: // parallelization with max 
        if (this->level->done){
            this->backpropagate((int)this->level->win, 1);
            this->available_actions.clear();
            return;
        }
        wins = this->level->rollout(-1, rollouts_per_leaf, 1) ? 1 : 0;
        break;
        case 2: // parallelization with avg
        if (this->level->done){
            this->backpropagate((int)this->level->win * rollouts_per_leaf, rollouts_per_leaf);
            this->available_actions.clear();
            return;
        }
        wins = this->level->rollout(-1, rollouts_per_leaf, 1);
        simulations = rollouts_per_leaf;
        break;
    }
    this->backpropagate(wins, simulations);
}
void Node::backpropagate(int wins, int simulations) {
    this->num_wins += wins;
    this->num_rollouts += simulations;
    if (this->parent != nullptr){
        this->parent->backpropagate(wins, simulations);
    }
}

void MicroNode::expand(Level& level){
    if (level.done) {
        return;
    }
    if (this->available_actions.size() == 0) {
        std::cout << "wtf" << std::endl;
        exit(0);
    }
    if (this->parent == nullptr) { // root node gets fully expanded 
        this->children.reserve(this->available_actions.size());
        for (auto action : this->available_actions) {
            MicroNode* child = new MicroNode(this, this->action_list, action);
            Level* cloned_level = level.clone();
            child->rollout(*cloned_level);
            // #pragma omp critical
            {
                this->children.push_back(child);
            } 
            delete cloned_level;
        }
        this->available_actions.clear();
        return;
    }
    int action_index = get_random_number(0, this->available_actions.size() - 1);
    Action chosen_action = this->available_actions[action_index];
    MicroNode* child = new MicroNode(this, this->action_list, chosen_action);
    child->rollout(level);
    this->children.push_back(child);
    this->available_actions.erase(this->available_actions.begin() + action_index);
}
void MicroNode::rollout(Level& level){
    for (auto action : this->action_list){
        level.deferred_step(action);
    }
    if (level.done){
        this->terminal = true;
        this->backpropagate((int)level.win);
        this->available_actions.clear();
        return;
    }
    this->backpropagate(level.rollout(1, 1, 1));
}
void MicroNode::backpropagate(int win){
    this->num_wins += win;
    this->num_rollouts++;
    if (this->parent != nullptr){
        this->parent->backpropagate(win);
    }
}
Node* select(Node& root){
    Node* current_node = &root;
    while(true){
        if(current_node->children.size() == 0){
            return current_node;
        }
        float best_ucb = 0;
        float ucb;
        Node* best_node = nullptr; // = current_node.children[0];
        for(Node* child : current_node->children){ // find non-terminal child with highest ucb
            if (child->terminal){
                continue;
            }
            ucb = child->ucb();
            if (ucb > best_ucb) {
                best_ucb = ucb;
                best_node = child;
            }
        }
        if (best_node == nullptr){ // all children nodes are terminal
            if (current_node->available_actions.size() > 0){
                return current_node;
            }
            else { // this node is fully expanded and is terminal
                return nullptr;
            }
        }
        if ((current_node->available_actions.size() > 0) && (best_ucb < current_node->ucb())){ // if this node can still be expanded and it has a higher ucb
            return current_node;
        }
        current_node = best_node;
    }
}

Action select_best_action(Node& root) {
    Action action = Action((PlantName)0,0,0);
    int most_rollouts = 0;
    int most_rollouts_wins = 0;
    for (auto node: root.children) {
        if (node->num_rollouts == most_rollouts && node->num_wins > most_rollouts_wins) {
            action = node->action;
            most_rollouts_wins = node->num_wins;
        }
        if (node->num_rollouts > most_rollouts) {
            most_rollouts_wins = node->num_wins;
            most_rollouts = node->num_rollouts;
            action = node->action;
        }
    }
    return action;
}
Action run(Level& level, int timeout_ms, int games_per_rollout, bool debug, float ucb_const, int mode){
    ucb_coefficient = ucb_const;
    rollouts_per_leaf = games_per_rollout;
    rollout_mode = mode;
    if (action_space.size() == 0){
        action_space = vector<Action>(level.get_action_space());
    }
    Node* root = new Node(nullptr, level, Action());
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    while(std::chrono::high_resolution_clock::now() < end_time && root->num_rollouts < 800000) {
        Node* next_node = select(*root);
        if (next_node == nullptr) {
            break;
        }
        next_node->expand();
    }
    Action chosen_action = select_best_action(*root);
    if (debug) {
        std::cout << "total expanded: " << root->num_rollouts << " total winrate: " << root->num_wins << std::endl;
    }
    delete root;
    return chosen_action;
}
// Action micro_run(Level& level, int timeout_ms, bool debug, float ucb_const){
//     ucb_coefficient = ucb_const;
//     if (action_space.size() == 0){
//         action_space = vector<Action>(level.get_action_space());
//     }    MicroNode* root = new MicroNode(nullptr, vector<Action>(), Action());
//     auto start_time = std::chrono::high_resolution_clock::now();
//     auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
//     while(std::chrono::high_resolution_clock::now() < end_time && root->num_rollouts < 800000) {
//         MicroNode* next_node = select<MicroNode>(*root);
//         if (next_node == nullptr) {
//             break;
//         }
//         Level* cloned_level = level.clone();
//         next_node->expand(*cloned_level);
//         delete cloned_level;
//     }
//     Action chosen_action = select_best_action<MicroNode>(*root);
//     if (debug) {
//         std::cout << "total expanded: " << root->num_rollouts << " total winrate: " << root->num_wins << std::endl;
//     }
//     delete root;
//     return chosen_action;
// }
int heuristic1(const Level& level)
{
    return (10 * level.count_plant(SUNFLOWER) + 5 * level.count_lawnmowers()) * level.frame;
}

int heuristic2(const Level& level)
{
    return (5 * level.count_plant(SUNFLOWER) + 4 * level.count_lawnmowers() + 2 * level.count_plant()) * level.frame;
}