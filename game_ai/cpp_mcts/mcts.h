#ifndef _MCTS
#define _MCTS
#include <list>
#include <vector>
#include <chrono>
#include "../cpp_env/level.hpp"
#include <math.h>
#include <omp.h>
#include <utility>
#include <algorithm>
using std::list;
using std::vector;

class Node;


class Node {
    public:
    int num_rollouts;
    double num_wins;
    const float ucb_coefficient;
    int rollouts_per_leaf;
    Level* level;
    Action action;
    Node* parent;
    vector<Node*> childern;
    vector<Action> available_actions;
    void expand();
    void backpropagate(double wins);
    void rollout();
    inline float ucb() const {
        if (this->level->done) {
            return 0;
        }
        if (this->num_rollouts == 0) { // MAX EXPLORE!
            return 100000;
        }
        // const float c = 1.4;
        int wins = this->num_wins;
        int rollouts = this->num_rollouts;
        int parent_rollouts;
        if (this->parent != nullptr) {
            parent_rollouts = this->parent->num_rollouts;
            if (parent_rollouts == 0) {
                // std::cout << "TODO SHOULDN'T GET HERE IMO?!!" << std::endl;
                return 0;
            }
        }
        else {
            parent_rollouts = this->num_rollouts;
        }
        float ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log(parent_rollouts) / rollouts));
        return ucb;
    };
    Node(Node* parent, Level& level, Action action, const float ucb_coefficient, int rollouts_per_leaf);
    Node* select();
    Node* select_with_heuristic();
    ~Node();
};

// Node& select_node(Node& root);
Action select_best_action(Node& root);
Action run(Level& level, int timeout_ms, int games_per_rollout, bool debug=false, float ucb_const=1.4);

int heuristic1(const Level& level);
int heuristic2(const Level& level);
// int heuristic3(Level& level);
// int heuristic4(Level& level);

#endif