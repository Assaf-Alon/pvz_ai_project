#ifndef _PVZ_LEVEL
#define _PVZ_LEVEL
#include <vector>
#include <string>
#include <list>
#include <array>
#include <deque>
#include <sstream>
#include <assert.h>
#include <iostream>
#include <random>
#include <functional>
#include <algorithm>
#include <omp.h>
#include <utility>
#include <chrono>
#include "plant.hpp"
using std::vector;
using std::string;
using std::pair;
using std::array;
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << std::endl;
#define FAST 7.5
#define SLOW 30
#define VERY_SLOW 50

#define FORCE_RANDOM 1
#define FORCE_DETERMINISTIC -1

inline int get_random_number(const int min, const int max){ 
    thread_local std::mt19937 generator(std::random_device{}());
    std::uniform_int_distribution<int> distribution(min, max);
    return distribution(generator);
}

inline double get_normal_sample(const double expected, const double variance) {
    thread_local std::mt19937 generator(std::random_device{}());
    std::normal_distribution<double> distribution(expected, variance);
    return distribution(generator);
}

class Level;
class Zombie;
class ZombieInfo;
class Plant;
typedef std::function<bool(Level&, Plant&)> PlantAction;
typedef std::function<double(const Level&)> heuristic_function;
typedef std::pair<int, int> Pos;

enum PlantName { NO_PLANT, CHERRYBOMB, CHOMPER,
                 HYPNOSHROOM, ICESHROOM, JALAPENO,
                 PEASHOOTER, POTATOMINE, PUFFSHROOM,
                 REPEATERPEA, SCAREDYSHROOM, SNOWPEA,
                 SPIKEWEED, SQUASH, SUNFLOWER,
                 SUNSHROOM, THREEPEATER, WALLNUT,
                 NUM_PLANTS };

// try to move it to plant.hpp
class PlantData {
    public:
    int hp;
    int damage;
    float action_interval_seconds;
    // int action_interval;
    float recharge_seconds;
    // int recharge;
    int cost;
    PlantAction action_func;
    std::string plant_name;
    int next_available_frame = 9999;
    int plant_type;
    PlantData() = default;
    PlantData(int hp, int damage, float action_interval_seconds, float recharge_seconds, int cost, PlantAction action_func, std::string plant_name, int plant_type) : \
    hp(hp), damage(damage), action_interval_seconds(action_interval_seconds), recharge_seconds(recharge_seconds), cost(cost), action_func(action_func), plant_name(plant_name), plant_type(plant_type) {};
};

static const std::array<PlantData, NUM_PLANTS> plant_data = {
        PlantData(0, 0, 0,   0,  0, PlantAction(&wallnut_action), "no_plant", NO_PLANT),
        PlantData(5000, 9000, 1.2,   50,  150, PlantAction(&cherrybomb_action), "cherrybomb", CHERRYBOMB),
        PlantData(300,  9000, 42,    7.5, 150, PlantAction(&chomper_action), "chomper", CHOMPER),
        PlantData(300,  20,   0,     30,  75,  PlantAction(&hypnoshroom_action), "hypnoshroom", HYPNOSHROOM),
        PlantData(5000, 20,   1,     50,  75,  PlantAction(&iceshroom_action), "iceshroom", ICESHROOM),
        PlantData(300,  9000, 1,     50,  125, PlantAction(&jalapeno_action), "jalapeno", JALAPENO),
        PlantData(300,  20,   1.425, 7.5, 100, PlantAction(&peashooter_action), "peashooter", PEASHOOTER),
        PlantData(300,  1800, 15,    30,  25,  PlantAction(&potatomine_action), "potatomine", POTATOMINE),
        PlantData(300,  20,   1.425, 7.5, 0,   PlantAction(&puffshroom_action), "puffshroom", PUFFSHROOM),
        PlantData(300,  20,   1.425, 7.5, 200, PlantAction(&repeaterpea_action), "repeaterpea", REPEATERPEA),
        PlantData(300,  20,   1.425, 7.5, 20,  PlantAction(&scaredyshroom_action), "scaredyshroom", SCAREDYSHROOM),
        PlantData(300,  20,   1.425, 7.5, 175, PlantAction(&snowpea_action), "snowpea", SNOWPEA),
        PlantData(300,  20,   1,     7.5, 100, PlantAction(&spikeweed_action), "spikeweed", SPIKEWEED),
        PlantData(300,  1800, 1.425, 30,  50,  PlantAction(&squash_action), "squash", SQUASH),
        PlantData(300,  25,   24.25, 7.5, 50,  PlantAction(&sunflower_action), "sunflower", SUNFLOWER),
        PlantData(300,  15,   24.25, 7.5, 25,  PlantAction(&sunshroom_action), "sunshroom", SUNSHROOM),
        PlantData(300,  20,   1.425, 7.5, 325, PlantAction(&threepeater_action), "threepeater", THREEPEATER),
        PlantData(4000, 0,    9999,  30,  50,  PlantAction(&wallnut_action), "wallnut", WALLNUT)
};

class ZombieSpawnTemplate {
    public:
    int second;
    int frame;
    int lane;
    int effective_lane;
    std::string type;
    ZombieSpawnTemplate() = default;
    ZombieSpawnTemplate(int second, int lane, std::string type): second(second), lane(lane), type(type) {
        frame = 0;
        effective_lane = lane;
    };
    bool operator< (const ZombieSpawnTemplate& other) {
        return this->frame < other.frame;
        // return this->second < other.second;
    }
};

// try to move to zombie.hpp
class ZombieInfo {
    public:
    int hp;
    string type;
    int lane;
    int col;
    bool frozen;
};

// try to move to plant.hpp
class PlantInfo {
    public:
    int hp;
    std::string plant_name;
    int lane;
    int col;
};

class Cell {
    public:
    PlantInfo plant_info;
    vector<ZombieInfo> zombie_info_vec;
    Cell() {
        this->zombie_info_vec = vector<ZombieInfo>();
    }
};

typedef vector<vector<Cell>> State;

class CellObservation {
    public:
    int plant_type;
    int plant_hp_phase;
    int zombie_danger_level;
    CellObservation(){
        this->plant_type = 0;
        this->plant_hp_phase = 0;
        this->zombie_danger_level = 0;
    }
    CellObservation(int plant_type, int plant_hp_phase, int zombie_danger_level) : 
        plant_type(plant_type), plant_hp_phase(plant_hp_phase), zombie_danger_level(zombie_danger_level) {};
    ~CellObservation() = default;
};

typedef vector<vector<vector<int>>> Observation;

class Action {
    public:
    int plant_name; // plant_name or none
    int lane;
    int col;
    Action(int name, int lane, int col) : plant_name(name), lane(lane), col(col) {};
    Action() = default;
    bool operator==(const Action& other) const {
        return this->plant_name == other.plant_name && this->lane == other.lane && this->col == other.col;
    }
    // Action& operator=(Action& action) = default;
};
struct ActionHash {
    std::size_t operator()(const Action& action) const {
        return std::hash<int>()(action.plant_name) ^ std::hash<int>()(action.lane) ^ std::hash<int>()(action.col);
    }
};
class Level {
public:
    int lanes;
    int cols;
    int suns = 50;
    int frame = 1;
    int last_sun_generated = 1;
    float sun_interval_seconds = 6; // Used to be 10
    int sun_interval;
    bool zombie_in_home_col = false;
    bool done = false;
    bool win = false;
    std::vector<bool> lawnmowers;
    int fps = 10;
    bool return_state = false;
    const Action no_action = Action(NO_PLANT, 0, 0);
    std::vector<int> chosen_plants;
    std::list<Zombie*> zombie_list;
    std::vector<std::vector<std::list<Zombie*>>> zombie_grid;
    std::list<Plant*> plant_list;
    std::vector<std::vector<Plant*>> plant_grid;
    std::deque<ZombieSpawnTemplate> level_data;
    std::vector<int> plant_cooldowns = std::vector<int>(9999, NUM_PLANTS);
    std::vector<Pos> free_spaces;
    bool randomize;


    // Constructors, copy, destructors
    Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate> level_data, vector<int> legal_plants, bool randomize=false);
    Level* clone(int clone_mode=0) const;
    Level(const Level& other_level);
    ~Level();
    void randomize_level_data(double variance=1.0);

    // Step and step-related
    void step(const Action& action);
    void step(int plant, int row, int col);
    void step();
    void deferred_step(const Action& action);
    private:
    void do_zombie_actions();
    void do_plant_actions();
    void do_player_action(const Action& action);
    void spawn_zombies();
    void spawn_suns();
    bool check_endgame();
    void plant(const Action& action);

    // Action related
    public:
    bool is_action_legal(const Action& action) const;
    bool is_action_legal(int plant, int row, int col) const;
    const Action get_random_action() const; // guranteed to be legal
    PlantName get_random_legal_plant() const;
    int get_random_plant() const;
    bool is_plantable(int plant) const;
    bool get_random_position(int& lane, int& col) const;
    vector<Pos>* get_all_legal_positions(); // for use in python
    vector<Action> get_action_space() const;

    // State/Observation
    Observation get_observation() const;
    State get_state() const;

    // misc
    void append_zombie(int second, int lane, std::string type);
    int rollout(int num_games=10000, int mode=1) const; // return num_victories
    std::pair<int, int> timed_rollout(int time_limit_ms, int mode = 1) const;

    int count_plant(PlantName target_plant) const;
    int count_lawnmowers() const;
    int count_plant() const;
};
bool play_random_game(const Level& env, int randomization_mode);
bool play_random_heuristic_game(Level env, heuristic_function& func, int mode=1);

#endif // _PVZ_LEVEL