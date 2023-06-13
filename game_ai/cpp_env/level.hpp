#ifndef _PVZ_LEVEL
#define _PVZ_LEVEL
#include <vector>
#include <string>
#include <list>
#include <deque>
#include <sstream>
#include <assert.h>
#include <iostream>
#include <random>
#include <memory>
#include <functional>
#include <algorithm>
#include <omp.h>
#include <utility>
#include <future>
#include <chrono>
using std::vector;
using std::string;
using std::pair;
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << std::endl;
#define FAST 7.5
#define SLOW 30
#define VERY_SLOW 50

int get_random_number(const int min, const int max);

class Level;
class Zombie;
class ZombieInfo;
class Plant;
typedef std::function<bool(Level&, Plant&)> PlantAction;
typedef std::pair<int, int> Pos;

// try to move it to plant.h
class PlantData {
    public:
    int hp;
    int damage;
    float action_interval_seconds;
    int action_interval;
    float recharge_seconds;
    int recharge;
    int cost;
    PlantAction action_func;
    std::string plant_name;
    int next_available_frame = 9999;
    int plant_type;
    PlantData() = default;
    PlantData(int fps, int hp, int damage, float action_interval_seconds, float recharge_seconds, int cost, PlantAction action_func, std::string plant_name, int plant_type) : \
    hp(hp), damage(damage), action_interval_seconds(action_interval_seconds), recharge_seconds(recharge_seconds), cost(cost), action_func(action_func), plant_name(plant_name), plant_type(plant_type) {
        this->action_interval = static_cast<int>(action_interval_seconds * fps);
        this->recharge = static_cast<int>(recharge_seconds * fps);
    };
};

enum PlantName { NO_PLANT, CHERRYBOMB, CHOMPER,
                 HYPNOSHROOM, ICESHROOM, JALAPENO,
                 PEASHOOTER, POTATOMINE, PUFFSHROOM,
                 REPEATERPEA, SCAREDYSHROOM, SNOWPEA,
                 SPIKEWEED, SQUASH, SUNFLOWER,
                 SUNSHROOM, THREEPEATER, WALLNUT,
                 NUM_PLANTS };

class ZombieSpawnTemplate {
    public:
    int second;
    int lane;
    std::string type;
    ZombieSpawnTemplate() = default;
    ZombieSpawnTemplate(int second, int lane, std::string type): second(second), lane(lane), type(type) {};
};

// try to move to zombie.h
class ZombieInfo {
    public:
    int hp;
    string type;
    int lane;
    int col;
    bool frozen;
};

// try to move to plant.h
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
    const PlantName plant_name; // plant_name or none
    int lane;
    int col;
    Action(PlantName name, int lane, int col) : plant_name(name), lane(lane), col(col) {}
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
    std::vector<PlantData> plant_data;
    std::vector<Pos> free_spaces;


    // Constructors, copy, destructors
    Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate> level_data, vector<int> legal_plants);
    Level* clone();
    Level(const Level& other_level);
    ~Level();

    // Step and step-related
    void step(const Action& action);
    void step(int plant, int row, int col);
    void step();
    void do_zombie_actions();
    void do_plant_actions();
    void do_player_action(const Action& action);
    void spawn_zombies();
    void spawn_suns();
    bool check_endgame();
    void plant(const Action& action);

    // Action related
    bool is_action_legal(const Action& action) const;
    bool is_action_legal(int plant, int row, int col) const;
    const Action get_random_action() const; // guranteed to be legal
    PlantName get_random_legal_plant() const;
    int get_random_plant() const;
    bool is_plantable(int plant) const;
    bool get_random_position(int& lane, int& col) const;
    vector<Pos>* get_all_legal_positions(); // for use in python

    // State/Observation
    Observation get_observation();
    State get_state();

    // misc
    void append_zombie(int second, int lane, std::string type);
    int rollout(int num_cpu, int num_games=10000, int mode=1); // return num_victories
    std::pair<int, int> timed_rollout(int num_cpu, int time_limit_ms, int mode = 1);
};
bool play_random_game(Level env, int randomization_mode);


#endif // _PVZ_LEVEL