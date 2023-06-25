#include "level.hpp"
#include "zombie.hpp"
#include "plant.hpp"

#include <unistd.h>

Zombie::Zombie(const std::string &type, int lane, const Level &level) : lane(lane), col(level.cols - 1), last_action(level.frame), type(type)
{
    if (type == "conehead")
    {
        this->hp = 551;
    }
    else if (type == "buckethead")
    {
        this->hp = 1281;
    }
    else if (type == "flag")
    {
        this->move_interval_seconds = 3.7;
    }
    else if (type == "newspaper")
    {
        this->hp = 331;
    }
    else if (type == "football")
    {
        this->hp = 1581;
        this->move_interval_seconds = 2.5;
    }
    else if (type == "pole")
    {
        this->can_jump = true;
        this->hp = 335;
        this->move_interval_seconds = 2.5;
    }
    this->move_interval = static_cast<int>(this->move_interval_seconds * level.fps);
    this->attack_interval = static_cast<int>(this->attack_interval_seconds * level.fps);
}
void Zombie::attack(Level &level)
{
    if ((level.frame - this->last_action) < this->attack_interval)
    {
        return;
    }
    Plant *target_plant = level.plant_grid[this->lane][this->col];
    if (target_plant == nullptr)
    {
        return;
    }
    // std::cout << "Zombie attacking! HP:" << this->hp << ", lane: " << this->lane << ", col: " << this->col << std::endl;
    if (this->can_jump) {
        #ifdef DEBUG
        std::stringstream log_msg;
        log_msg << this->type << " zombie at " << this->lane << ", " << this->col << " has vaulted!";
        LOG_FRAME(level.frame, log_msg.str());
        #endif
        this->vault(level);
        return;
    }
#ifdef DEBUG
    std::stringstream log_msg;
    log_msg << this->type << " zombie at " << this->lane << ", " << this->col << " attacked";
    LOG_FRAME(level.frame, log_msg.str());
#endif
    this->last_action = level.frame;
    target_plant->get_damaged(this->damage, level);
}
void Zombie::move(Level &level)
{
    if ((level.frame - this->last_action) < this->move_interval)
    {
        return;
    }
    this->last_action = level.frame;
    if (this->col == 0)
    {
        level.zombie_in_home_col = true;
        this->entering_house = true;
    }
    else
    {
#ifdef DEBUG
        std::stringstream log_msg;
        log_msg << this->type << " zombie at " << this->lane << ", " << this->col << " moved";
        LOG_FRAME(level.frame, log_msg.str());
#endif
        level.zombie_grid[this->lane][this->col].remove(this);
        this->col -= 1;
        level.zombie_grid[this->lane][this->col].push_back(this);
    }
}
void Zombie::do_action(Level &level)
{
    this->attack(level);
    this->move(level);
}
void Zombie::get_damaged(int damage, Level &level)
{
    this->hp -= damage;
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << this->type << " zombie at " << this->lane << ", " << this->col << " sustained " << damage << " damage. HP: " << std::to_string(this->hp);
    LOG_FRAME(level.frame, log_msg.str());
    #endif
    if (this->type == "newspaper")
    {
        if (this->hp <= 181)
        {
            #ifdef DEBUG
            std::stringstream log_msg;
            log_msg << this->type << " zombie at " << this->lane << ", " << this->col << " lost newspaper";
            LOG_FRAME(level.frame, log_msg.str());
            #endif
            this->type = "lost_newspaper"; // danger zone with strings
            this->move_interval = 1.8 * level.fps;
        }
    }
    if (this->hp <= 0)
    {
        // remove self from both global and cell lists
        #ifdef DEBUG
        std::stringstream log_msg;
        log_msg << this->type << " zombie at " << this->lane << ", " << this->col << " died";
        LOG_FRAME(level.frame, log_msg.str());
        #endif
        level.zombie_grid[this->lane][this->col].remove(this);
        level.zombie_list.remove(this);
        delete this;
    }
}
void Zombie::vault(Level& level){
    this->can_jump = false;
    if (this->col == 0){
        level.zombie_in_home_col = true;
    }
    else if (this->col > 0) {
        level.zombie_grid[this->lane][this->col].remove(this);
        this->col -= 1;
        level.zombie_grid[this->lane][this->col].push_back(this);
    }
    this->last_action = level.frame;
    this->move_interval_seconds = 4.7;
    this->move_interval = static_cast<int>(this->move_interval_seconds * level.fps);
}

ZombieInfo Zombie::get_info(){
    ZombieInfo info;
    info.hp = this->hp;
    info.type = this->type;
    info.lane = this->lane;
    info.col = this->col;
    info.frozen = this->frozen;
    return info;
}