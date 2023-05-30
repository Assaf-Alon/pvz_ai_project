#include <vector>
#include <string>
#include <list>
#include <deque>
#include <sstream>
#include <assert.h>
#include <iostream>
#include <random>
#include <memory>
#include <algorithm>
using std::vector;
using std::string;
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << std::endl;

class Level;
class Zombie;
class Plant;

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
    Plant(int lane, int column, int frame, int fps);
    virtual void do_action(Level& level) = 0;
    void get_damaged(int damage, Level& level);
    virtual Plant* clone() const = 0;
    virtual ~Plant() = default;
};

// class Cherrybomb : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Cherrybomb(int lane, int column, int frame, int fps);
//     virtual Cherrybomb* clone() const override;
//     ~Cherrybomb() = default;
// };

// class Chomper : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Chomper(int lane, int column, int frame, int fps);
//     virtual Chomper* clone() const override;
//     ~Chomper() = default;
// };

// class Iceshroom : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Iceshroom(int lane, int column, int frame, int fps);
//     virtual Iceshroom* clone() const override;
//     ~Iceshroom() = default;
// };

// class Jalapeno : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Jalapeno(int lane, int column, int frame, int fps);
//     virtual Jalapeno* clone() const override;
//     ~Jalapeno() = default;
// };

class Peashooter : public Plant {
    public:
    void do_action(Level& level) override;
    Peashooter(int lane, int column, int frame, int fps);
    Peashooter* clone() const override;
    ~Peashooter() = default;
};

// class Potatomine : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Potatomine(int lane, int column, int frame, int fps);
//     virtual Potatomine* clone() const override;
//     ~Potatomine() = default;
// };

// class Puffshroom : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Puffshroom(int lane, int column, int frame, int fps);
//     virtual Puffshroom* clone() const override;
//     ~Puffshroom() = default;
// };

// class Repeaterpea : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Repeaterpea(int lane, int column, int frame, int fps);
//     virtual Repeaterpea* clone() const override;
//     ~Repeaterpea() = default;
// };

// class Scaredyshroom : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Scaredyshroom(int lane, int column, int frame, int fps);
//     virtual Scaredyshroom* clone() const override;
//     ~Scaredyshroom() = default;
// };

// class Snowpea : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Snowpea(int lane, int column, int frame, int fps);
//     virtual Snowpea* clone() const override;
//     ~Snowpea() = default;
// };

// class Spikeweed : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Spikeweed(int lane, int column, int frame, int fps);
//     virtual Spikeweed* clone() const override;
//     ~Spikeweed() = default;
// };

// class Squash : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Squash(int lane, int column, int frame, int fps);
//     virtual Squash* clone() const override;
//     ~Squash() = default;
// };

class Sunflower : public Plant {
    public:
    void do_action(Level& level) override;
    Sunflower(int lane, int column, int frame, int fps);
    Sunflower* clone() const override;
    ~Sunflower() = default;
};

// class Sunshroom : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Sunshroom(int lane, int column, int frame, int fps);
//     virtual Sunshroom* clone() const override;
//     ~Sunshroom() = default;
// };

// class Threepeater : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Threepeater(int lane, int column, int frame, int fps);
//     virtual Threepeater* clone() const override;
//     ~Threepeater() = default;
// };

// class Wallnut : public Plant {
//     public:
//     void do_action(Level& level) override;
//     Wallnut(int lane, int column, int frame, int fps);
//     virtual Wallnut* clone() const override {
//         Wallnut* cloned = new Wallnut(lane, col, last_action, fps);
//         return cloned;
//     }
//     ~Wallnut() = default;
// };

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
    std::string plant_name; // plant_name or none
    int lane;
    int col;
    Action(std::string name, int lane, int col) : plant_name(name), lane(lane), col(col) {}
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
    std::string get_random_plant();
    bool get_random_position(int& lane, int& col);
    void plant(const Action& action);
    // void remove_plant(int lane, int col);

    static bool play_random_game(Level env);
};