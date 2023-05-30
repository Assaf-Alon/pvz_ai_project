#include "level.h"

Plant::Plant(int lane, int column, int frame, int fps) : lane(lane), col(column), last_action(frame), fps(fps) {}

void Plant::get_damaged(int damage, Level &level)
{
    this->hp -= damage;
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "Plant at " << this->lane << ", " << this->col << " sustained " << damage << " damage. HP: " << std::to_string(this->hp);
    LOG_FRAME(level.frame, log_msg.str());
    #endif
    if (this->hp <= 0)
    {
        level.plant_list.remove(this);
        level.plant_grid[this->lane][this->col] = nullptr;
        #ifdef DEBUG
        std::stringstream log_msg;
        log_msg << "Plant at " << this->lane << ", " << this->col << " died";
        LOG_FRAME(level.frame, log_msg.str());
        LOG_FRAME(level.frame, " >> Plants left: " + std::to_string(level.plant_list.size()));
        #endif
        delete this; // this is a really bad idea and needs to be fixed by moving to smart ptrs
    }
}

//========================================
//Sunflower 
//========================================

Sunflower::Sunflower(int lane, int column, int frame, int fps) : Plant(lane, column, frame, fps)
{
    this->hp = 300;
    this->damage = 25;
    this->action_interval_seconds = 24.25;
    this->action_interval = static_cast<int>(this->action_interval_seconds * fps);
    this->recharge_seconds = 7.5;
    this->recharge = static_cast<int>(this->recharge_seconds * fps);
    this->cost = 50;
}

void Sunflower::do_action(Level &level)
{
    if (level.frame - this->last_action <= this->action_interval)
    {
        return;
    }
    this->last_action = level.frame;
    level.suns += this->damage;
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "Plant at " << this->lane << ", " << this->col << " generated sun. total: " + std::to_string(level.suns);
    LOG_FRAME(level.frame, log_msg.str());
    #endif
}

Sunflower* Sunflower::clone() const {
    Sunflower* cloned = new Sunflower(lane, col, last_action, fps);
    return cloned;
}

//========================================
//Peashooter 
//========================================

Peashooter::Peashooter(int lane, int column, int frame, int fps) : Plant(lane, column, frame, fps)
{
    this->hp = 300;
    this->damage = 20;
    this->action_interval_seconds = 1.425;
    this->action_interval = static_cast<int>(this->action_interval_seconds * fps);
    this->recharge_seconds = 7.5;
    this->recharge = static_cast<int>(this->recharge_seconds * fps);
    this->cost = 100;
}
void Peashooter::do_action(Level &level)
{
    if (level.frame - this->last_action <= this->action_interval)
    {
        return;
    }
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "Plant at " << this->lane << ", " << this->col << " attacked";
    LOG_FRAME(level.frame, log_msg.str());
    #endif
    this->last_action = level.frame;
    for (int i = 0; i < level.cols; i++)
    {
        Zombie *target_zombie = level.zombie_grid[this->lane][i].front();
        if (target_zombie == nullptr)
        {
            continue;
        }
        target_zombie->get_damaged(this->damage, level);
        break;
    }
}

Peashooter* Peashooter::clone() const {
    Peashooter* cloned = new Peashooter(lane, col, last_action, fps);
    // std::cout << "Cloned Peashooter at " << lane << ", " << col << std::endl;
    return cloned;
}

//========================================
//Cherrybomb 
//========================================

// Cherrybomb::Cherrybomb(int lane, int column, int frame, int fps): Plant(lane, column, frame, fps)
// {
//     this->hp = 9998;
//     this->damage = 1800;
//     this->action_interval_seconds = 1.2;
//     this->action_interval = static_cast<int>(this->action_interval_seconds * fps); // action interval of bomb is arm time
//     this->recharge_seconds = 50;
//     this->recharge = static_cast<int>(this->recharge_seconds * fps);
//     this->cost = 150;
// }
// void Cherrybomb::do_action(Level& level){
//     if(level.frame - this->last_action <= this->action_interval){
//         return;
//     }
//     //explode
//     for (int i = -1; i <= 1; i++){
//         int target_lane = this->lane + i;
//         if (target_lane <= 0 || target_lane >= level.lanes){
//             continue;
//         }
//         for (int j = -1; j <= 1; j++){
//             int target_col = this->col + j;
//             if(target_col <= 0 || target_col >= level.cols){
//                 continue;
//             }
//             std::list<Zombie*> cell = level.zombie_grid[target_lane][target_col];
//             for (auto zombie : cell){
//                 zombie->get_damaged(this->damage, level);
//             }
//         }
//     }
//     this->get_damaged(9999, level);
// }

// Cherrybomb* Cherrybomb::clone() const {
//     return new Cherrybomb(this->lane, this->col, this->last_action, this->fps);
// }
