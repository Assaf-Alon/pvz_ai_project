#include <vector>
#include <string>
#include <list>
#include <deque>
#include <sstream>
#include <assert.h>
#include <iostream>
#include <random>
using std::vector;
using std::string;
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << std::endl;

class Level;
class Zombie;
class Plant;


// class Zombie2Spawn {
// public:
//     int frame;
//     int lane;
//     Zombie2Spawn(int frame, int lane) {
//         this->frame = frame;
//         this->lane = lane;
//     }
// };
class ZombieSpawnTemplate {
    public:
    int second;
    int lane;
    std::string type;
};
// typedef struct zombie2be_spawned {
//     int frame;
//     int lane;
// } Zombie2Spawn;

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
    Plant(int lane, int column, int frame, int fps);
    virtual void do_action(Level& level) = 0;
    void get_damaged(int damage, Level& level);
    virtual Plant* clone() const = 0;
};

class Sunflower : public Plant {
    public:
    void do_action(Level& level) override;
    Sunflower(int lane, int column, int frame, int fps);
    virtual Sunflower* clone() const override {
        Sunflower* cloned = new Sunflower(lane, col, last_action, fps);
        // std::cout << "Cloned sunflower at " << lane << ", " << col << std::endl;
        return cloned;
    }
};

class Peashooter : public Plant {
    public:
    void do_action(Level& level) override;
    Peashooter(int lane, int column, int frame, int fps);
    virtual Peashooter* clone() const override {
        Peashooter* cloned = new Peashooter(lane, col, last_action, fps);
        // std::cout << "Cloned Peashooter at " << lane << ", " << col << std::endl;
        return cloned;
    }
};

class State {

};
class Action {
    public:
    std::string plant_name; // plant_name or none
    int lane;
    int col;
    Action(std::string name, int lane, int col) : plant_name(name), lane(lane), col(col) {}
};
class Level {
public:
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
    bool *lawnmowers;
    int fps = 10;
    bool return_state = false;
    std::list<Zombie*> zombie_list;
    std::list<Zombie*>** zombie_grid;
    std::list<Plant*> plant_list;
    Plant*** plant_grid;
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

    std::vector<int>& rollout(int num_cpu); // return num_victories, num_losses? (DIFFICULTY: MEDIUM)
    Action get_random_action(); // guranteed to be legal (DIFFICULTY: MEDIUM)
    int get_random_uniform(int min, int max);
    std::string get_random_plant();
    bool get_random_position(std::string plant_name, int* lane, int* col);
    
    void plant(const Action& action);
    // void remove_plant(int lane, int col);
};