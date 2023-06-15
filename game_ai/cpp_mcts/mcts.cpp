#include "mcts.h"


inline void print_action(Action& action, Level& level){
    std::cout << "chosen action: " << level.plant_data[action.plant_name].plant_name << " at " << action.lane << ", " << action.col << std::endl;
    
}

inline int _get_random_number(const int min, const int max){ 
    static std::mt19937 generator(std::random_device{}());
    std::uniform_int_distribution<int> distribution(min, max);
    return distribution(generator);
}

Node::Node(Node* parent, Level& level, Action action) {
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
    Node* best_node = nullptr;
    #pragma omp parallel for
    for (auto child : this->childern) {
        if (child->level->done) continue;
        ucb = child->ucb();
        #pragma omp critical
        if (ucb > best_ucb) {
            best_ucb = ucb;
            best_node = child;
        }
    }
    if (best_ucb < this->ucb() && this->available_actions.size() > 0){
        return this;
    }
    if (best_node == nullptr) {
        return nullptr;
    }
    best_node = best_node->select();
    if (best_node == nullptr && this->available_actions.size() > 0){
        return this;
    }
    return best_node->select();

}
void Node::expand(int num_rollouts) {
    if (this->available_actions.size() == 0) {
        std::cout << "wtf" << std::endl;
        exit(0);
    }
    if (this->parent == nullptr) { // root node gets fully expanded 
        for (auto action : this->available_actions) {
            Node* child = new Node(this, *this->level, action);
            child->rollout(num_rollouts);
            this->childern.push_back(child);
        }
        this->available_actions.clear();
        return;
    }
    int action_index = _get_random_number(0, this->available_actions.size() - 1);
    Action chosen_action = this->available_actions[action_index];
    Node* child = new Node(this, *this->level, chosen_action);
    child->rollout(num_rollouts);
    this->childern.push_back(child);
    this->available_actions.erase(this->available_actions.begin() + action_index);

}
void Node::rollout(int num_rollouts) {
    while (!this->level->is_action_legal(action) && !(this->level->done)) this->level->step();
    if (this->level->done){
        this->backpropagate(this->level->win, 1);
        return;
    }
    this->level->step(this->action);
    // static const int rollout = 12;
    int win = this->level->rollout(8, num_rollouts, 1);
    this->backpropagate(win, num_rollouts);
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
    float best_ucb = 0;
    // int most_rollouts = 0;
    for (auto node: root.childern) {
        // print_action(node->action, *root.level);
        // std::cout << node->ucb() << std::endl;
        // std::cout << "wins: " << node->num_wins << " rollouts: " << node->num_rollouts << " parennt rollouts: " << node->parent->num_rollouts << std::endl;
        // std::cout << "==============================" << std::endl;
        if (node->ucb() > best_ucb) {
            best_ucb = node->ucb();
            action = node->action;
        }
    }
    return action;
}
Action run(Level& level, int timeout, int games_per_rollout){
    omp_set_num_threads(8);
    Node root = Node(nullptr, level, Action((PlantName)0,0,0));
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::seconds(timeout);
    while(std::chrono::high_resolution_clock::now() < end_time) {
        Node* next_node = root.select();
        if (next_node == nullptr) {
            break;
        }
        next_node->expand(games_per_rollout);
    }
    Action chosen_action = select_best_action(root);
    return chosen_action;
}
int main() {
    omp_set_num_threads(8);
    std::vector<int> chosen_plants = {SUNFLOWER, PEASHOOTER, POTATOMINE, SQUASH, SPIKEWEED, WALLNUT};
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(11, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(12, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(50, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(85, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(11, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(12, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(50, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(85, 1, "normal"));
    Level level = Level(5, 10, 10, level_data, chosen_plants);
    while (!level.done){
        Node root = Node(nullptr, level, Action((PlantName)0,0,0));
        int wins = level.rollout(8, 10000, 1);
        std::cout << "win rate before: " << 100 * (float)wins / 10000 << "%" << std::endl;
        auto start_time = std::chrono::high_resolution_clock::now();
        auto end_time = start_time + std::chrono::seconds(1);
        int expanded = 0;
        while(std::chrono::high_resolution_clock::now() < end_time) {
            Node* next_node = root.select();
            if (next_node == nullptr) {
                std::cout << "returned nullptr from select" << std::endl;
                break;
            }
            next_node->expand(28);
            expanded++;
        }
        Action chosen_action = select_best_action(root);
        std::cout << "chosen action: " << level.plant_data[chosen_action.plant_name].plant_name << " at " << chosen_action.lane << ", " << chosen_action.col << std::endl;
        while (!level.is_action_legal(chosen_action) && !level.done) level.step();
        if (level.done){
            break;
        }
        level.step(chosen_action);
        wins = level.rollout(8, 10000, 1);
        std::cout << "win rate after: " << 100 * (float)wins / 10000 << "%" << std::endl;
        std::cout << "current frame: " << level.frame << std::endl;
        std::cout << "total rollouts: " << root.num_rollouts << std::endl;
        std::cout << "expanded nodes: " << expanded << std::endl;
        std::cout << "=============================================" << std::endl;
    }
    std::cout << "game ended with status: " << (level.done ? "win" : "loss") << " at frame: " << level.frame << std::endl;
}