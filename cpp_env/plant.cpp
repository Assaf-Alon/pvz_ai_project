#include "level.h"

Plant::Plant(int lane, int column, int frame, int fps, PlantName plant_name, std::function<void(Level&, Plant&)> action) : lane(lane), col(column), last_action(frame), fps(fps), action(action) {
    if (plant_name == CHERRYBOMB){
        this->hp = 5000;
        this->damage = 9000;
        this->action_interval_seconds = 0;
        this->recharge_seconds = 50;
        this->cost = 150;
    }
    else if (plant_name == CHOMPER) {
        this->hp = 300;
        this->damage = 9999;
        this->action_interval_seconds = 42;
        this->recharge_seconds = 7.5;
        this->cost = 150;
    }
    else if (plant_name == HYPNOSHROOM) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 0;
        this->recharge_seconds = 30;
        this->cost = 75;
    }
    else if (plant_name == ICESHROOM) {
        this->hp = 5000;
        this->damage = 9999;
        this->action_interval_seconds = 0;
        this->recharge_seconds = 50;
        this->cost = 75;
    }
    else if (plant_name == JALAPENO) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1;
        this->recharge_seconds = 50;
        this->cost = 125;
    }
    else if (plant_name == "peashooter") {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 100;
    }
    else if (plant_name == POTATOMINE) {
        this->hp = 300;
        this->damage = 1800;
        this->action_interval_seconds = 15;
        this->recharge_seconds = 30;
        this->cost = 25;
    }
    else if (plant_name == PUFFSHROOM) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 0;
    }
    else if (plant_name == REPEATERPEA) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 200;
    }
    else if (plant_name == SCAREDYSHROOM) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 25;
    }
    else if (plant_name == SNOWPEA) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 175;
    }
    else if (plant_name == SPIKEWEED) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1;
        this->recharge_seconds = 7.5;
        this->cost = 100;
    }
    else if (plant_name == SQUASH) {
        this->hp = 300;
        this->damage = 1800;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 30;
        this->cost = 50;
    }
    else if (plant_name == "sunflower") {
        this->hp = 300;
        this->damage = 25;
        this->action_interval_seconds = 24.25;
        this->recharge_seconds = 7.5;
        this->cost = 50;
    }
    else if (plant_name == SUNSHROOM) {
        this->hp = 300;
        this->damage = 15; // After two minutes - 25
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 25;
    }
    else if (plant_name == THREEPEATER) {
        this->hp = 300;
        this->damage = 20;
        this->action_interval_seconds = 1.425;
        this->recharge_seconds = 7.5;
        this->cost = 325;
    }
    else if (plant_name == WALLNUT) {
        this->hp = 4000;
        this->damage = 0;
        this->action_interval_seconds = 9999;
        this->recharge_seconds = 30;
        this->cost = 50;
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
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "Plant at " << this->lane << ", " << this->col << " attacked";
    LOG_FRAME(level.frame, log_msg.str());
    #endif
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
            while(!cell.empty()){
                cell.front()->get_damaged(plant.damage, level);
            }
        }
    }
    plant.get_damaged(9999, level); // self destruct
}
void chomper_action(Level& level, Plant& plant){
    for (int pos_mod = 0; pos_mod <= 1; pos_mod++){
        if (plant.col + pos_mod >= level.cols){
            continue;
        }
        std::list<Zombie*> cell = level.zombie_grid[plant.lane][plant.col + pos_mod];
        if(!cell.empty()){
            plant.last_action = level.frame;
            cell.front()->get_damaged(plant.damage, level);
            return;
        }
    }
}
void hypnoshroom_action(Level& level, Plant& plant){
    return;
}
void iceshroom_action(Level& level, Plant& plant){
    return;
}
void jalapeno_action(Level& level, Plant& plant){
    for (int col = 0; col < level.cols; col++){
        std::list<Zombie*> cell = level.zombie_grid[plant.lane][col];
        while(!cell.empty()){
            cell.front()->get_damaged(plant.damage, level);
        }
    }
    plant.get_damaged(9999, level); // self destruct
}
void peashooter_action(Level& level, Plant& plant){
    for (int i = plant.col; i < level.cols; i++)
    {
        Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
        if (target_zombie == nullptr)
        {
            continue;
        }
        target_zombie->get_damaged(plant.damage, level);
        plant.last_action = level.frame;
        return;
    }
}
void potatomine_action(Level& level, Plant& plant){
    std::list<Zombie*> cell = level.zombie_grid[plant.lane][plant.col];
    if(cell.empty()){
        return;
    }
    while(!cell.empty()){
        cell.front()->get_damaged(plant.damage, level);
    }
    plant.get_damaged(9999, level); // self destruct
}
void puffshroom_action(Level& level, Plant& plant){
    return;
}
void repeaterpea_action(Level& level, Plant& plant){
    for (int shots = 0; shots <= 1; shots++){ // shoots twice
        for (int i = plant.col; i < level.cols; i++)
        {
            Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
            if (target_zombie == nullptr)
            {
                continue;
            }
            plant.last_action = level.frame;
            target_zombie->get_damaged(plant.damage, level);
            break;
        }
    }
}
void scaredyshroom_action(Level& level, Plant& plant){
    return;
}
void snowpea_action(Level& level, Plant& plant){
    for (int i = plant.col; i < level.cols; i++)
    {
        Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
        if (target_zombie == nullptr)
        {
            continue;
        }
        target_zombie->get_damaged(plant.damage, level);
        // target_zombie->get_frozen(); !!!!
        plant.last_action = level.frame;
        break;
    }
}
void spikeweed_action(Level& level, Plant& plant){
    plant.last_action = level.frame;
    std::list<Zombie*> cell = level.zombie_grid[plant.lane][plant.col];
    while (!cell.empty()){
        cell.front()->get_damaged(plant.damage, level);
    }

}
void squash_action(Level& level, Plant& plant){
    for (int pos_mod = 0; pos_mod <= 1; pos_mod++){
        if (plant.col + pos_mod >= level.cols){
            continue;
        }
        std::list<Zombie*> cell = level.zombie_grid[plant.lane][plant.col + pos_mod];
        if(cell.empty()){
            // important! if you remove this, the plant will delete itself without damaging anything
            continue;
        }
        while(!cell.empty()){
            cell.front()->get_damaged(plant.damage, level);
        }
        plant.get_damaged(9999, level);
        return;
    }
}
void sunflower_action(Level& level, Plant& plant){
    plant.last_action = level.frame;
    level.suns += plant.damage;
}
void sunshroom_action(Level& level, Plant& plant){
    return;
}
void threepeater_action(Level& level, Plant& plant){
    for (int lane_mod = -1; lane_mod <= 1; lane_mod++){
        if(plant.lane + lane_mod <= 0 || plant.lane + lane_mod >= level.lanes){
            continue;
        }
        for (int i = plant.col; i < level.cols; i++)
        {
            Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
            if (target_zombie == nullptr)
            {
                continue;
            }
            target_zombie->get_damaged(plant.damage, level);
            plant.last_action = level.frame;
            break;
        }
    }
}
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
