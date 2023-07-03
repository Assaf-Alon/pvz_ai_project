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
// extern int rollout_mode;

class Node;

class Node {
    public:
    int simulations;
    int wins;
    bool terminal;
    Level* level;
    Node* parent;
    Action action;
    vector<Node*> children;
    vector<Action> available_actions;
    inline double ucb(int rollout_mode) const {
        if (this->level->done) {
            return int(this->level->win);
        }
        if (this->simulations == 0) { // MAX EXPLORE!
            std::cout << "reched ucb with 0 rollouts, should this be possible??" << std::endl;
            return 100000;
        }
        int wins = this->wins;
        int rollouts = this->simulations;
        int parent_rollouts;
        if (this->parent != nullptr) {
            parent_rollouts = this->parent->simulations;
            if (parent_rollouts == 0) {
                std::cout << "TODO SHOULDN'T GET HERE IMO?!!" << std::endl;
                return 0;
            }
        }
        else {
            parent_rollouts = this->simulations;
        }
        double ucb;
        if (rollout_mode == 2){
            ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log((double)parent_rollouts / rollouts_per_leaf) / (rollouts / rollouts_per_leaf)));
        }
        else {
            ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log(parent_rollouts) / rollouts));
        }
        return ucb;
    };
    Node(Node* parent, Level& level, Action action) : parent(parent), action(action) {
        this->terminal = false;
        this->simulations = 0;
        this->wins = 0;
        this->available_actions = vector<Action>(action_space);
        this->level = level.clone(1);
        this->children.reserve(this->available_actions.size());
    };
    ~Node() {
        delete level;
        for (auto node : children) {
            delete node;
        }
    };
};
Node* select(Node* root, int rollout_mode);
Node* expand(Node* selected_node);
void rollout(Node* selected_node, int rollout_mode);
void backpropagate(Node* selected_node);

// Node& select_node(Node& root);
std::pair<Action, int> select_best_action(Node& root);
Action run(Level& level, int timeout_ms, int games_per_rollout, bool debug=false, float ucb_const=1.4, int rollout_mode=0);
Action parralel_run(Level& level, int timeout_ms, int parralel_factor, bool debug, float ucb_const);
// Node* select(Node& root);
// Action micro_run(Level& level, int timeout_ms, bool debug, float ucb_const=1.4);
int heuristic1(const Level& level);
int heuristic2(const Level& level);
// int heuristic3(Level& level);
// int heuristic4(Level& level);

#endif