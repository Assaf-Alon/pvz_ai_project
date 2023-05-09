#include <vector>
#include <string>
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

typedef struct zombie_data {
    bool alive;
    int lane;
    int col;
    int hp;
    int damage;
    // int type_code;
    int move_interval;
    int attack_interval;
    int last_action;
    bool entering_house;
    // bool frozen;
    // bool hypnotized;
} Zombie_data;

typedef struct plant_data {
    int lane;
    int col;
    int hp;
    int damage;
    int attack_interval;
    int sun_interval;
    int last_action;
} Plant_data;

class Zombie {
public:
    Zombie_data* data;
    Zombie* next;
    Zombie* prev;
    Zombie(int lane, int column, Level* level);
    void attack(Level* level);
    void move(Level* level);
    void do_action(Level* level);
    void get_damaged(int damage, Level* Levels);
};

class Plant {
public:
    Plant_data* data;
    Plant* next;
    Plant* prev;
    bool isSunflower;
    Plant(int lane, int column);
    Plant(int lane, int column, bool isSunflower);
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
    Zombie_data zombie_data_array[1024];
    Plant* plant_list_head;
    Zombie* zombie_list_head;
    vector<Zombie2Spawn> zombies_to_spawn;
    // Zombie

    Level(int lanes, int columns, int fps);
    bool step(string plant_type, int lane, int col);
    
    void plant(int lane, int column, bool isSunflower);
    // void remove_plant(int lane, int col);
};