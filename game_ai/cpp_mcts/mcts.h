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

#define NORMAL_MCTS 0
#define MAX_NODE 1
#define AVG_NODE 2
#define PARALLEL_TREES 3
#define NO_HEURISTIC 0
#define HEURISTIC_MCTS 1
#define HEURISTIC_SELECT 2
#define HEURISTIC_EXPAND 3
// #define NUM_CPU 8
typedef std::function<double(const Level&, const Action&)> heuristic_function;

extern float ucb_coefficient;
extern int rollouts_per_leaf;
static vector<Action> action_space;
extern int rollout_mode;
extern int max_depth;
// extern heuristic_function h_func;


class Node;

class Node {
    public:
    int simulations;
    int wins;
    bool terminal;
    Node* parent;
    Action action;
    vector<Node*> children;
    vector<Action> available_actions;
    inline double ucb() const {
        // TODO: check if this is correct
        // if (level.done) {
        //     return int(level.win);
        // }
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
        if (rollout_mode == AVG_NODE){ //
            ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log((double)parent_rollouts / rollouts_per_leaf) / (rollouts / rollouts_per_leaf)));
        }
        else {
            ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(log(parent_rollouts) / rollouts));
        }
        return ucb;
    };
    Node(Node* parent, Action action) : parent(parent), action(action) {
        this->terminal = false;
        this->simulations = 0;
        this->wins = 0;
        this->available_actions = vector<Action>(action_space);
        this->children.reserve(this->available_actions.size());
    };
    ~Node() {
        for (auto node : children) {
            delete node;
        }
    };
};

Node* select(Node* root, Level& cloned_level, bool use_heuristic=false);
Node* expand(Node* selected_node, Level& cloned_level, bool use_heuristic=false);
void rollout(Node* selected_node, Level& cloned_level);
void backpropagate(Node* start_node);

std::pair<Action, int> select_best_action(Node& root);
Action run(Level& level, int timeout_ms, int simulations_per_leaf, bool debug=false, float ucb_const=1.4, int mode=NORMAL_MCTS, int heuristic_mode=NO_HEURISTIC);
Action _parallel_trees_run(Level& level, int timeout_ms, int num_trees, bool debug, int heurisic_mode);
double heuristic_basic_sunflowers(const Level& level, const Action& action);

inline float heuristic2(const Level& level)
{
    double x = (5 * level.count_plant(SUNFLOWER) + 4 * level.count_lawnmowers() + 2 * level.count_plant());
    return x / (1 + abs(x)); // * level.frame;
}
#endif