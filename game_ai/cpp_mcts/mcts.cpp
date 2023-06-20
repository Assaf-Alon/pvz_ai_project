#include "mcts.h"

inline void print_action(Action& action, Level& level){
    std::cout << "chosen action: " << plant_data[action.plant_name].plant_name << " at " << action.lane << ", " << action.col << std::endl;
    
}

Node::Node(Node* parent, Level& level, Action action, const float ucb_coefficient): ucb_coefficient(ucb_coefficient) {
    static const vector<Action> action_space = vector<Action>(level.get_action_space()); // populate using level
    this->available_actions = vector<Action>(action_space);
    this->action = action;
    this->parent = parent;
    this->level = level.clone();
    this->childern.reserve(this->available_actions.size());
}
Node* Node::select() {
    if (this->childern.size() == 0) {
        return this;
    }
    float best_ucb = 0;
    float ucb;
    Node* best_node = this->childern[0];
    for (auto child : this->childern) {
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
void Node::expand(int num_rollouts) {
    if (this->level->done) {
        return;
    }
    if (this->available_actions.size() == 0) {
        std::cout << "wtf" << std::endl;
        exit(0);
    }
    if (this->parent == nullptr) { // root node gets fully expanded 
        for (auto action : this->available_actions) {
            Node* child = new Node(this, *this->level, action, this->ucb_coefficient);
            child->rollout(num_rollouts);
            this->childern.push_back(child);
        }
        this->available_actions.clear();
        return;
    }
    int action_index = get_random_number(0, this->available_actions.size() - 1);
    Action chosen_action = this->available_actions[action_index];
    Node* child = new Node(this, *this->level, chosen_action, this->ucb_coefficient);
    child->rollout(num_rollouts);
    this->childern.push_back(child);
    this->available_actions.erase(this->available_actions.begin() + action_index);

}
void Node::rollout(int num_rollouts) {
    while (!this->level->is_action_legal(this->action) && !(this->level->done)) {
        this->level->step();
    }
    if (this->level->done){
        this->backpropagate((int)this->level->win, 1);
        this->available_actions.clear();
        return;
    }
    this->level->step(this->action);
    int wins = this->level->rollout(1, num_rollouts, 1);
    this->backpropagate(wins, num_rollouts);
}
void Node::backpropagate(int wins, int rollouts) {
    this->num_wins += wins;
    this->num_rollouts += rollouts;
    if (this->parent != nullptr){
        this->parent->backpropagate(wins, rollouts);
    }
}
Node::~Node() {
    delete level;
    for (auto node : childern) {
        delete node;
    }
}

Action select_best_action(Node& root) {
    Action action = Action((PlantName)0,0,0);
    int most_rollouts = 0;
    int most_rollouts_wins = 0;
    for (auto node: root.childern) {
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
    omp_set_num_threads(8);
    Node root = Node(nullptr, level, Action((PlantName)0,0,0), ucb_const);
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(timeout_ms);
    while(std::chrono::high_resolution_clock::now() < end_time && root.num_rollouts < 200000) {
        Node* next_node = root.select();
        if (next_node == nullptr) {
            break;
        }
        next_node->expand(games_per_rollout);
    }
    Action chosen_action = select_best_action(root);
    if (debug) {
        std::cout << "total expanded: " << root.num_rollouts << std::endl;
    }
    return chosen_action;
}