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


static float ucb_coefficient;
static int rollouts_per_leaf;

class Node;

class Node {
    public:
    int num_rollouts;
    int num_wins;
    Level* level;
    Action action;
    Node* parent;
    vector<Node*> children;
    vector<Action> available_actions;
    void expand();
    void backpropagate(int wins);
    virtual void rollout();
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
    Node(Node* parent, Level& level, Action action);
    virtual Node* select();
    // Node* select_with_heuristic();
    virtual ~Node();
};
class ParallelNode : public Node {
    public:
    ParallelNode(ParallelNode* parent, Level& level, Action action): Node(parent, level, action){};
    void rollout() override;
};

// Node& select_node(Node& root);
Action select_best_action(Node& root);
Action run(Level& level, int timeout_ms, int games_per_rollout, bool debug=false, float ucb_const=1.4);
Node* select(Node& root);
int heuristic1(const Level& level);
int heuristic2(const Level& level);
// int heuristic3(Level& level);
// int heuristic4(Level& level);

#endif