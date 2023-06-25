#ifndef _MCTS
#define _MCTS
#include <list>
#include <vector>
#include <chrono>
#include "../cpp_env/level.hpp"
#include <math.h>
#include <omp.h>
// #include <utility>
// #include <algorithm>
using std::list;
using std::vector;


extern float ucb_coefficient;
extern int rollouts_per_leaf;
static vector<Action> action_space;
extern int rollout_mode;

class Node;

class Node {
    public:
    int num_rollouts;
    int num_wins;
    bool terminal;
    Level* level;
    Node* parent;
    Action action;
    vector<Node*> children;
    vector<Action> available_actions;
    void expand();
    void backpropagate(int wins, int simulations);
    void rollout();
    inline double ucb() const {
        if (this->level->done) {
            return 0;
        }
        if (this->num_rollouts == 0) { // MAX EXPLORE!
            std::cout << "reched ucb with 0 rollouts, should this be possible??" << std::endl;
            return 100000;
        }
        int wins = this->num_wins;
        int rollouts = this->num_rollouts;
        int parent_rollouts;
        if (this->parent != nullptr) {
            parent_rollouts = this->parent->num_rollouts;
            if (parent_rollouts == 0) {
                std::cout << "TODO SHOULDN'T GET HERE IMO?!!" << std::endl;
                return 0;
            }
        }
        else {
            parent_rollouts = this->num_rollouts;
        }
        double ucb;
        if (rollout_mode == 2){
            ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log((double)parent_rollouts / rollouts_per_leaf) / (rollouts * rollouts_per_leaf)));
        }
        else {
            ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log(parent_rollouts) / rollouts));
        }
        return ucb;
    };
    Node(Node* parent, Level& level, Action action) : parent(parent), action(action) {
        this->terminal = false;
        this->num_rollouts = 0;
        this->num_wins = 0;
        this->available_actions = vector<Action>(action_space);
        this->level = level.clone();
        this->children.reserve(this->available_actions.size());
    };
    // virtual Node* select();
    // Node* select_with_heuristic();
    ~Node() {
        delete level;
        for (auto node : children) {
            delete node;
        }
    };
};
class MicroNode {
    public:
    int num_rollouts;
    int num_wins;
    bool terminal;
    MicroNode* parent;
    vector<Action> action_list;
    Action action;
    vector<MicroNode*> children;
    vector<Action> available_actions;
    inline float ucb() const {
        if (this->num_rollouts == 0) { // MAX EXPLORE!
            return 100000;
        }
        int wins = this->num_wins;
        int rollouts = this->num_rollouts;
        int parent_rollouts;
        if (this->parent != nullptr) {
            parent_rollouts = this->parent->num_rollouts;
        }
        else {
            parent_rollouts = this->num_rollouts;
        }
        float ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log(parent_rollouts) / rollouts));
        return ucb;
    };
    MicroNode(MicroNode* parent, vector<Action> action_list, Action node_action): parent(parent), action_list(action_list), action(node_action) {
        this->action_list.push_back(node_action);
        this->available_actions = vector<Action>(action_space);
        this->num_rollouts = 0;
        this->num_wins = 0;
        this->terminal = false;
    };
    ~MicroNode() {
        for (auto child : this->children){
            delete child;
        }
    };
    void expand(Level& level);
    void rollout(Level& level);
    void backpropagate(int win);
};

Node* select(Node& root);

// Node& select_node(Node& root);
Action select_best_action(Node& root);
Action run(Level& level, int timeout_ms, int games_per_rollout, bool debug=false, float ucb_const=1.4, int mode=0);
// Node* select(Node& root);
// Action micro_run(Level& level, int timeout_ms, bool debug, float ucb_const=1.4);
int heuristic1(const Level& level);
int heuristic2(const Level& level);
// int heuristic3(Level& level);
// int heuristic4(Level& level);

#endif