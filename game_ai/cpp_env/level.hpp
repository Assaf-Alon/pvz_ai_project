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
#include <unordered_map>
#include <functional>
#include <algorithm>
#include <omp.h>
using std::vector;
using std::string;
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << std::endl;
#define FAST 7.5
#define SLOW 30
#define VERY_SLOW 50

int get_random_number(const int min, const int max);

class Level;
class Zombie;
class Plant;
typedef std::function<bool(Level&, Plant&)> PlantAction;

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
    // PlantData(const PlantData& other) = default;
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
// enum PlantName {NO_PLANT, PEASHOOTER, SUNFLOWER, SQUASH, WALLNUT, POTATOMINE, SPIKEWEED, NUM_PLANTS};

// typedef std::string PlantName;

class ZombieSpawnTemplate {
    public:
    int second;
    int lane;
    std::string type;
    ZombieSpawnTemplate() = default;
    ZombieSpawnTemplate(int second, int lane, std::string type): second(second), lane(lane), type(type) {};
};

class ZombieInfo {
    public:
    int hp;
    string type;
    int lane;
    int col;
    bool frozen;
};

class Zombie {
    public:
    int lane;
    int col;
    int hp = 181;
    int damage = 100;
    double move_interval_seconds = 4.7;
    int move_interval;
    double attack_interval_seconds = 1.0;
    int attack_interval;
    int last_action;
    bool entering_house = false;
    string type;
    bool frozen = false;
    bool hypnotized = false;
    Zombie(const string& type, int lane, const Level& level);
    Zombie(const Zombie& other) = default;
    void attack(Level& level);
    void move(Level& level);
    void do_action(Level& level);
    void get_damaged(int damage, Level& Levels);
    ZombieInfo get_info();
};

class PlantInfo {
    public:
    int hp;
    std::string plant_name;
    int lane;
    int col;
};

class Plant {
public:
    int lane;
    int col;
    int hp;
    int cost;
    int damage; // for sun-generating plants, this is the value of the sun generated
    float action_interval_seconds;
    int action_interval;
    float recharge_seconds;
    int recharge;
    int frame_action_available;
    int fps;   // for clone...?
    int plant_type;
    std::string plant_name;
    Plant(int lane, int column, PlantData &plant_data, int frame, int fps);
    PlantAction action;
    PlantInfo get_info();
    void do_action(Level& level);
    void get_damaged(int damage, Level& level);
    Plant* clone() const;
    ~Plant() = default;
};

bool cherrybomb_action(Level& level, Plant& plant);
bool chomper_action(Level& level, Plant& plant);
bool hypnoshroom_action(Level& level, Plant& plant);
bool iceshroom_action(Level& level, Plant& plant);
bool jalapeno_action(Level& level, Plant& plant);
bool peashooter_action(Level& level, Plant& plant);
bool potatomine_action(Level& level, Plant& plant);
bool puffshroom_action(Level& level, Plant& plant);
bool repeaterpea_action(Level& level, Plant& plant);
bool scaredyshroom_action(Level& level, Plant& plant);
bool snowpea_action(Level& level, Plant& plant);
bool spikeweed_action(Level& level, Plant& plant);
bool squash_action(Level& level, Plant& plant);
bool sunflower_action(Level& level, Plant& plant);
bool sunshroom_action(Level& level, Plant& plant);
bool threepeater_action(Level& level, Plant& plant);
bool wallnut_action(Level& level, Plant& plant);

class Cell {
    public:
    PlantInfo plant_info;
    vector<ZombieInfo> zombie_info_vec;
    Cell() {
        // this->plant_info = nullptr;
        this->zombie_info_vec = vector<ZombieInfo>();
    }
    // ~Cell() {
    //     if (this->plant_info != nullptr){
    //         delete plant_info;
    //     }
    // }
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

typedef vector<vector<CellObservation>> Observation;

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
    float sun_interval_seconds = 10;
    int sun_interval;
    bool zombie_in_home_col = false;
    bool done = false;
    bool win = false;
    std::vector<bool> lawnmowers;
    int fps = 10;
    bool return_state = false;
    std::list<Zombie*> zombie_list;
    std::vector<std::vector<std::list<Zombie*>>> zombie_grid;
    std::list<Plant*> plant_list;
    std::vector<std::vector<Plant*>> plant_grid;
    std::deque<ZombieSpawnTemplate> level_data;
    std::vector<PlantData> plant_data;

    Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate> level_data, vector<int> legal_plants);
    Level* clone();
    Level(const Level& other_level);
    ~Level();
    void step(const Action& action);
    void step(int plant, int row, int col);
    void do_zombie_actions();
    void do_plant_actions();
    void do_player_action(const Action& action);
    void spawn_zombies();
    void spawn_suns();
    bool check_endgame();
    bool is_action_legal(const Action& action) const;
    void append_zombie(int second, int lane, std::string type);
    Observation get_observation();
    State get_state();

    int rollout(int num_cpu, int num_games=10000); // return num_victories
    const Action get_random_action() const; // guranteed to be legal
    PlantName get_random_plant() const;
    bool get_random_position(int& lane, int& col) const;
    void plant(const Action& action);
    // void remove_plant(int lane, int col);
    const Action no_action = Action(NO_PLANT, 0, 0);

    static bool play_random_game(Level env);
};


#endif // _PVZ_LEVEL