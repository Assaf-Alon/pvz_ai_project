#include <vector>
#include <string>
#include <list>
using std::vector;
using std::string;

class Level;
class Zombie;
class Plant;


class Zombie2Spawn {
public:
    int frame;
    int lane;
    Zombie2Spawn(int frame, int lane) {
        this->frame = frame;
        this->lane = lane;
    }
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
    // int type_code;
    int move_interval = 5;
    int attack_interval = 1;
    int last_action;
    bool entering_house = false;
    // bool frozen;
    // bool hypnotized;
    Zombie(int lane, int column, Level* level);
    void attack(Level* level);
    void move(Level* level);
    void do_action(Level* level);
    void get_damaged(int damage, Level* Levels);
};

class Plant {
public:
    int lane;
    int col;
    int hp = 0;
    int damage = 0;
    int action_interval = 0;
    int last_action;
    bool isSunflower;
    Plant(int lane, int column, int frame, bool isSunflower);
    void attack(Level* level);
    void generate_sun(Level* level);
    void do_action(Level* level);
    void get_damaged(int damage, Level* level);
};


class Level {
public:
    int lanes;
    int cols;
    int suns;
    int frame;
    int last_sun_generated;
    bool zombie_in_home_col;
    bool done;
    bool win;
    bool *lawnmowers;
    int fps = 10;
    std::list<Zombie*> zombie_list;
    std::list<Zombie*>** zombie_grid;
    std::list<Plant*> plant_list;
    Plant*** plant_grid;
    vector<Zombie2Spawn> zombies_to_spawn;

    Level(int lanes, int columns, int fps);
    ~Level();
    bool step(const string &plant_type, int lane, int col);
    void do_zombie_actions();
    void do_plant_actions();
    void do_player_action(const string &plant_name, int lane, int col);
    void spawn_zombies();
    void spawn_suns();
    void check_endgame();
    bool is_action_legal(const string &plant_name, int lane, int col);

    
    void plant(int lane, int column, bool isSunflower);
    // void remove_plant(int lane, int col);
};