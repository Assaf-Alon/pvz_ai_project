#include "level.h"

Plant::Plant(int lane, int column, int frame, int fps, PlantName plant_name, std::function<void(Level&, Plant&)> action) : lane(lane), col(column), last_action(frame), fps(fps), action(action) {
    if (plant_name == SUNFLOWER) {
        this->hp = 300;
        this->damage = 25;
        this->action_interval_seconds = 24.25;
        this->recharge_seconds = 7.5;
        this->cost = 50;
    }
    else if (plant_name == PEASHOOTER) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 100;
    }
    this->action_interval = static_cast<int>(this->action_interval_seconds * fps);
    this->recharge = static_cast<int>(this->recharge_seconds * fps);
}

Plant* Plant::clone() const{
    return new Plant(*this);
}

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

void Plant::do_action(Level& level){
    if (level.frame - this->last_action <= this->action_interval)
    {
        return;
    }
    this->action(level, *this);
}

void cherrybomb_action(Level& level, Plant& plant){
    //explode
    for (int i = -1; i <= 1; i++){
        int target_lane = plant.lane + i;
        if (target_lane <= 0 || target_lane >= level.lanes){
            continue;
        }
        for (int j = -1; j <= 1; j++){
            int target_col = plant.col + j;
            if(target_col <= 0 || target_col >= level.cols){
                continue;
            }
            std::list<Zombie*> cell = level.zombie_grid[target_lane][target_col];
            for (auto zombie : cell){
                zombie->get_damaged(plant.damage, level);
            }
        }
    }
    plant.get_damaged(9999, level);
}
void chomper_action(Level& level, Plant& plant);
void hypnoshroom_action(Level& level, Plant& plant);
void iceshroom_action(Level& level, Plant& plant);
void jalapeno_action(Level& level, Plant& plant);
void peashooter_action(Level& level, Plant& plant){
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "Plant at " << plant.lane << ", " << plant.col << " attacked";
    LOG_FRAME(level.frame, log_msg.str());
    #endif
    plant.last_action = level.frame;
    for (int i = 0; i < level.cols; i++)
    {
        Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
        if (target_zombie == nullptr)
        {
            continue;
        }
        target_zombie->get_damaged(plant.damage, level);
        break;
    }
}
void potatomine_action(Level& level, Plant& plant);
void puffshroom_action(Level& level, Plant& plant);
void repeaterpea_action(Level& level, Plant& plant);
void scaredyshroom_action(Level& level, Plant& plant);
void snowpea_action(Level& level, Plant& plant);
void spikeweed_action(Level& level, Plant& plant);
void squash_action(Level& level, Plant& plant);
void sunflower_action(Level& level, Plant& plant){
    plant.last_action = level.frame;
    level.suns += plant.damage;
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "Plant at " << plant.lane << ", " << plant.col << " generated sun. total: " + std::to_string(level.suns);
    LOG_FRAME(level.frame, log_msg.str());
    #endif
}
void sunshroom_action(Level& level, Plant& plant);
void threepeater_action(Level& level, Plant& plant);
void wallnut_action(Level& level, Plant& plant){
    return;
}




// //========================================
// //Sunflower 
// //========================================

// Sunflower::Sunflower(int lane, int column, int frame, int fps) : Plant(lane, column, frame, fps)
// {
//     this->hp = 300;
//     this->damage = 25;
//     this->action_interval_seconds = 24.25;
//     this->action_interval = static_cast<int>(this->action_interval_seconds * fps);
//     this->recharge_seconds = 7.5;
//     this->recharge = static_cast<int>(this->recharge_seconds * fps);
//     this->cost = 50;
// }

// void Sunflower::do_action(Level &level)
// {
//     if (level.frame - this->last_action <= this->action_interval)
//     {
//         return;
//     }
//     this->last_action = level.frame;
//     level.suns += this->damage;
//     #ifdef DEBUG
//     std::stringstream log_msg;
//     log_msg << "Plant at " << this->lane << ", " << this->col << " generated sun. total: " + std::to_string(level.suns);
//     LOG_FRAME(level.frame, log_msg.str());
//     #endif
// }

// Sunflower* Sunflower::clone() const {
//     Sunflower* cloned = new Sunflower(lane, col, last_action, fps);
//     return cloned;
// }

// //========================================
// //Peashooter 
// //========================================

// Peashooter::Peashooter(int lane, int column, int frame, int fps) : Plant(lane, column, frame, fps)
// {
//     this->hp = 300;
//     this->damage = 20;
//     this->action_interval_seconds = 1.425;
//     this->action_interval = static_cast<int>(this->action_interval_seconds * fps);
//     this->recharge_seconds = 7.5;
//     this->recharge = static_cast<int>(this->recharge_seconds * fps);
//     this->cost = 100;
// }
// void Peashooter::do_action(Level &level)
// {
//     if (level.frame - this->last_action <= this->action_interval)
//     {
//         return;
//     }
//     #ifdef DEBUG
//     std::stringstream log_msg;
//     log_msg << "Plant at " << this->lane << ", " << this->col << " attacked";
//     LOG_FRAME(level.frame, log_msg.str());
//     #endif
//     this->last_action = level.frame;
//     for (int i = 0; i < level.cols; i++)
//     {
//         Zombie *target_zombie = level.zombie_grid[this->lane][i].front();
//         if (target_zombie == nullptr)
//         {
//             continue;
//         }
//         target_zombie->get_damaged(this->damage, level);
//         break;
//     }
// }

// Peashooter* Peashooter::clone() const {
//     Peashooter* cloned = new Peashooter(lane, col, last_action, fps);
//     // std::cout << "Cloned Peashooter at " << lane << ", " << col << std::endl;
//     return cloned;
// }

// //========================================
// //Cherrybomb 
// //========================================

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
