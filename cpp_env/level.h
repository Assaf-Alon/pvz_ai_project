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
using std::vector;
using std::string;
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << std::endl;

class Level;
class Zombie;
class Plant;

enum PlantName { NO_PLANT, PEASHOOTER, SUNFLOWER, CHERRYBOMB };

class ZombieSpawnTemplate {
    public:
    int second;
    int lane;
    std::string type;
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
    // Zombie(int lane, int column, Level* level);
    Zombie(const string& type, int lane, const Level& level);
    Zombie(const Zombie& other) = default;
    void attack(Level& level);
    void move(Level& level);
    void do_action(Level& level);
    void get_damaged(int damage, Level& Levels);
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
    int last_action;
    int fps;   // for clone...?
    Plant(int lane, int column, int frame, int fps, PlantName plant_name, const std::function<void(Level&, Plant&)> action);
    // virtual void do_action(Level& level) = 0;
    std::function<void(Level&, Plant&)> action;
    void do_action(Level& level);
    void get_damaged(int damage, Level& level);
    // virtual Plant* clone() const = 0;
    Plant* clone() const;
    ~Plant() = default;
};

void cherrybomb_action(Level& level, Plant& plant);
void chomper_action(Level& level, Plant& plant);
void hypnoshroom_action(Level& level, Plant& plant);
void iceshroom_action(Level& level, Plant& plant);
void jalapeno_action(Level& level, Plant& plant);
void peashooter_action(Level& level, Plant& plant);
void potatomine_action(Level& level, Plant& plant);
void puffshroom_action(Level& level, Plant& plant);
void repeaterpea_action(Level& level, Plant& plant);
void scaredyshroom_action(Level& level, Plant& plant);
void snowpea_action(Level& level, Plant& plant);
void spikeweed_action(Level& level, Plant& plant);
void squash_action(Level& level, Plant& plant);
void sunflower_action(Level& level, Plant& plant);
void sunshroom_action(Level& level, Plant& plant);
void threepeater_action(Level& level, Plant& plant);
void wallnut_action(Level& level, Plant& plant);

/*
Cherrybomb
Chomper
HypnoShroom (fuck)
Iceshroom
Jalapeno
[DONE] Peashooter
Potatomine
Puffshroom
Repeaterpea
Scaredyshroom
Snowpea
Spikeweed (fuck)
Squash
[DONE] Sunflower
Sunshroom
Threepeater
Wallnut
*/

class State {

};
class Action {
    public:
    PlantName plant_name; // plant_name or none
    int lane;
    int col;
    Action(PlantName name, int lane, int col) : plant_name(name), lane(lane), col(col) {}
};
class Level {
public:
    std::mt19937 random_gen;
    int delete_me_action_probability = 100; // TODO - delete this (not yet tho)
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
    // bool *lawnmowers;
    std::vector<bool> lawnmowers;
    int fps = 10;
    bool return_state = false;
    // Initialize the lists before the grids to make lifetime of lists longer
    // this will make the unique_ptrs to call the destructors after the grid itself leaves scope
    // ensuring correct order of deletion of plants and zombies
    std::list<Zombie*> zombie_list;
    // std::list<Zombie*> zombie_list;
    std::vector<std::vector<std::list<Zombie*>>> zombie_grid;
    // std::list<Zombie*>** zombie_grid;
    std::list<Plant*> plant_list;
    // std::list<Plant*> plant_list;
    std::vector<std::vector<Plant*>> plant_grid;
    // Plant*** plant_grid;
    // std::list<Zombie2Spawn> zombies_to_spawn;
    std::deque<ZombieSpawnTemplate> level_data;

    Level();
    Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate>& level_data);
    Level(const Level& other_level); // copy constructor (DIFFUCULTY: HELL)
    ~Level();
    State* step(const Action& action);
    void do_zombie_actions();
    void do_plant_actions();
    void do_player_action(const Action& action);
    void spawn_zombies();
    void spawn_suns();
    bool check_endgame();
    bool is_action_legal(const Action& action);

    int rollout(int num_cpu, int num_games=10000); // return num_victories
    Action get_random_action(); // guranteed to be legal (DIFFICULTY: MEDIUM)
    int get_random_uniform(int min, int max);
    PlantName get_random_plant();
    bool get_random_position(int& lane, int& col);
    void plant(const Action& action);
    // void remove_plant(int lane, int col);

    static bool play_random_game(Level env);
};