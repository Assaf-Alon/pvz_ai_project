#ifndef _PVZ_ZOMBIE
#define _PVZ_ZOMBIE
#include <string>
#include <vector>
class Level;

class ZombieInfo;

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
    std::string type;
    bool frozen = false;
    bool hypnotized = false;
    Zombie(const std::string& type, int lane, const Level& level);
    Zombie(const Zombie& other) = default;
    void attack(Level& level);
    void move(Level& level);
    void do_action(Level& level);
    void get_damaged(int damage, Level& Levels);
    ZombieInfo get_info();
};

#endif