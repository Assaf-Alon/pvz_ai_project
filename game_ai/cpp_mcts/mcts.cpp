#include "mcts.h"

inline void print_action(Action& action, Level& level){
    std::cout << "chosen action: " << plant_data[action.plant_name].plant_name << " at " << action.lane << ", " << action.col << std::endl;
    
}
static vector<Action> action_space; //  = vector<Action>(level.get_action_space()); // populate using level

Node::Node(Node* parent, Level& level, Action action) {
    this->num_rollouts = 0;
    this->num_wins = 0;
    this->available_actions = vector<Action>(action_space);
    this->action = action;
    this->parent = parent;
    this->level = level.clone();
    this->children.reserve(this->available_actions.size());
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

Node* Node::select() {
    if (this->children.size() == 0) {
        return this;
    }
    float best_ucb = 0;
    float ucb;
    Node* best_node = this->children[0];
    for (auto child : this->children) {
        ucb = child->ucb();
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
    best_node = best_node->select(); // recursive select node
    
    // Child leads to finished game, there're still actions to expand here
    if (best_node == nullptr && this->available_actions.size() > 0){
        return this;
    }
    return best_node;
}

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
    if (this->level->done){
        this->backpropagate((int)this->level->win);
        this->available_actions.clear();
        return;
    }
    int wins = this->level->rollout(-1, 1, 1);
    this->backpropagate(wins);
}
void ParallelNode::rollout(){
    this->level->deferred_step(this->action);
    if (this->level->done){
        this->backpropagate((int)this->level->win);
        this->available_actions.clear();
        return;
    }
    int wins = 0;
    if (this->level->rollout(8, rollouts_per_leaf, 1) > 0){
        wins = 1;
    }
    this->backpropagate(wins);
}
void Node::backpropagate(int wins) {
    this->num_wins += wins;
    this->num_rollouts++;
    if (this->parent != nullptr){
        this->parent->backpropagate(wins);
    }
}
Node::~Node() {
    delete level;
    for (auto node : children) {
        delete node;
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
        for(auto child : current_node->children){ // find non-terminal child with highest ucb
            if (child->level->done){
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
                return current_node; // can create more children at this node
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
Action run(Level& level, int timeout_ms, int games_per_rollout, bool debug, float ucb_const){
    // omp_set_num_threads(8);
    // omp_set_dynamic(1);
    ucb_coefficient = ucb_const;
    rollouts_per_leaf = games_per_rollout;
    action_space = vector<Action>(level.get_action_space());
    Node* root;
    if (games_per_rollout == 1){
        root = new Node(nullptr, level, Action());
    }
    else {
        root = new ParallelNode(nullptr, level, Action());
    }
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    while(std::chrono::high_resolution_clock::now() < end_time && root->num_rollouts < 800000) {
        // Node* next_node = root.select();
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

int heuristic1(const Level& level)
{
    return (10 * level.count_plant(SUNFLOWER) + 5 * level.count_lawnmowers()) * level.frame;
}

int heuristic2(const Level& level)
{
    return (5 * level.count_plant(SUNFLOWER) + 4 * level.count_lawnmowers() + 2 * level.count_plant()) * level.frame;
}