#ifndef _MCTS
#define _MCTS
#include <list>
#include <vector>
#include <chrono>
#include "../game_engine/level.hpp"
#include <math.h>
#include <omp.h>
// #include <utility>
// #include <algorithm>
using std::list;
using std::vector;

// modes
#define NORMAL_MCTS 0
#define MAX_NODE 1
#define AVG_NODE 2
#define PARALLEL_TREES 3

// heuristic modes
#define NO_HEURISTIC 0
#define HEURISTIC_SELECT 1

// selection modes
#define FULL_EXPAND 0 // fully expand each node before selecting chilrden
#define SQUARE_RATIO 1 // chance of descent is square of ratio between total actions and available actions
// #define LINEAR_RATIO 2 // chance of descent is linear of ratio between total actions and available actions
// #define ROOT_FULL_EXPAND 3 // fully expand root, descent freely later

// loss heuristic modes
#define NO_HEURISTIC 0
#define FRAME_HEURISTIC 1
#define TOTAL_PLANT_COST_HEURISTIC 2
#define TOTAL_ZOMBIE_HP_HEURISTIC 3
#define ZOMBIES_LEFT_TO_SPAWN_HEURISTIC 4


#define EXPAND_BATCH 8
typedef std::function<double(const Level&, const Action&)> heuristic_function;

extern float ucb_coefficient;
extern int rollouts_per_leaf;
static vector<Action> action_space;
static int action_space_size;
extern int rollout_mode;
extern int max_depth;
extern int selection_mode;
// extern bool use_loss_heuristic;
// extern heuristic_function h_func;


class Node;

class Node {
    public:
    int simulations;
    double wins;
    bool terminal;
    Node* parent;
    Action action;
    vector<Node*> children;
    vector<Action> available_actions;
    inline double ucb() const {
        if (this->simulations == 0) { // MAX EXPLORE!
            // std::cout << "reched ucb with 0 rollouts, should this be possible??" << std::endl;
            return 100000;
        }
        int wins = this->wins;
        int rollouts = this->simulations;
        int parent_rollouts;
        if (this->parent != nullptr) {
            parent_rollouts = this->parent->simulations;
            if (parent_rollouts == 0) {
                // std::cout << "SHOULDN'T GET HERE IMO?!!" << std::endl;
                return 0;
            }
        }
        else {
            parent_rollouts = this->simulations;
        }
        double ucb;
        if (rollout_mode == AVG_NODE){ //
            static double log_rollouts_per_leaf = log(rollouts_per_leaf);
            ucb = ((double)wins / rollouts) + (ucb_coefficient * sqrt(((log(parent_rollouts) - log_rollouts_per_leaf) * rollouts_per_leaf) / rollouts));
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
Node* expand(Node* selected_node, Level& cloned_level);
void rollout(Node* selected_node, Level& cloned_level);
void backpropagate(Node* start_node);

std::pair<Action, int> select_best_action(Node& root);
Action run(Level& level, int timeout_ms, int simulations_per_leaf, bool debug=false, float ucb_const=1.4, int mode=NORMAL_MCTS, int heuristic_mode=NO_HEURISTIC, int selection_type=FULL_EXPAND, int loss_heuristic=NO_HEURISTIC);
Action _parallel_trees_run(Level& level, int timeout_ms, int num_trees, bool debug, int heurisic_mode);
double heuristic_basic_sunflowers(const Level& level, const Action& action);

inline float heuristic2(const Level& level)
{
    double x = (5 * level.count_plant(SUNFLOWER) + 4 * level.count_lawnmowers() + 2 * level.count_plant());
    return x / (1 + abs(x)); // * level.frame;
}
#endif