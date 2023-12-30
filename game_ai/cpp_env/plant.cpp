#include "level.hpp"
#include "zombie.hpp"
#include "plant.hpp"

Plant::Plant(int lane, int column, const PlantData& plant_data, int frame, int fps){
    this->hp = plant_data.hp;
    this->damage = plant_data.damage;
    // this->action_interval_seconds = plant_data.action_interval_seconds;
    this->action_interval = plant_data.action_interval_seconds * fps;
    // this->recharge_seconds = plant_data.recharge_seconds;
    this->recharge = plant_data.recharge_seconds * fps;
    this->cost = plant_data.cost;
    this->lane = lane;
    this->col = column;
    this->plant_name = std::string(plant_data.plant_name);
    this->action = PlantAction(plant_data.action_func);
    this->plant_type = plant_data.plant_type;
    
    // TODO - pretty much all plants but the comper should start as-if they just attacked,
    // that is, they should wait before they attack.
    // The string comparation here sucks.
    // Maybe Keep the enum value inside PlantData?
    this->frame_action_available = frame + this->action_interval;
    if (this->plant_type == CHOMPER) {
        this->frame_action_available = frame;
    }

    // Sunflower's first sun generated takes about 6 seconds
    if (this->plant_type == SUNFLOWER) {
        this->frame_action_available = frame + (6*fps);
    }
}

Plant* Plant::clone() const{
    return new Plant(*this);
}

void Plant::get_damaged(int damage, Level &level)
{
    this->hp -= damage;
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << this->plant_name << " at " << this->lane << ", " << this->col << " sustained " << damage << " damage. HP: " << std::to_string(this->hp);
    LOG_FRAME(level.frame, log_msg.str());
    #endif
    if (this->hp <= 0)
    {
        level.plant_list.remove(this);
        level.plant_grid[this->lane][this->col] = nullptr;
        level.free_spaces.push_back(Pos(this->lane, this->col));
        #ifdef DEBUG
        std::stringstream log_msg;
        log_msg << this->plant_name << " at " << this->lane << ", " << this->col << " died";
        LOG_FRAME(level.frame, log_msg.str());
        LOG_FRAME(level.frame, " >> Plants left: " + std::to_string(level.plant_list.size()));
        #endif
        delete this; // this is a really bad idea and needs to be fixed by moving to smart ptrs
    }
}

void Plant::do_action(Level& level){
    // if (level.frame - this->last_action <= this->action_interval)
    if(level.frame < this->frame_action_available)
    {
        return;
    }
    // this doesnt work well because some plants self destruct...
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << this->plant_name << " at " << this->lane << ", " << this->col << " attacked";
    bool attacked = this->action(level, *this);
    if(attacked){
        LOG_FRAME(level.frame, log_msg.str());
    }
    #else
    this->action(level, *this);
    #endif
}
PlantInfo Plant::get_info(){
    PlantInfo plant_info;
    plant_info.hp = this->hp;
    plant_info.lane = this->lane;
    plant_info.col = this->col;
    plant_info.plant_name = this->plant_name;
    return plant_info;
}

bool cherrybomb_action(Level& level, Plant& plant){
    //explode
    for (int i = -1; i <= 1; i++){
        int target_lane = plant.lane + i;
        if (target_lane < 0 || target_lane >= level.lanes){
            continue;
        }
        for (int j = -1; j <= 1; j++){
            int target_col = plant.col + j;
            if(target_col < 0 || target_col >= level.cols){
                continue;
            }
            std::list<Zombie*> &cell = level.zombie_grid[target_lane][target_col];
            while(!cell.empty()){
                cell.front()->get_damaged(plant.damage, level);
            }
        }
    }
    plant.get_damaged(9999, level); // self destruct
    return true;
}
bool chomper_action(Level& level, Plant& plant){
    for (int pos_mod = 0; pos_mod <= 1; pos_mod++){
        if (plant.col + pos_mod >= level.cols){
            continue;
        }
        std::list<Zombie*> &cell = level.zombie_grid[plant.lane][plant.col + pos_mod];
        if(!cell.empty()){
            plant.frame_action_available = level.frame + plant.action_interval;
            cell.front()->get_damaged(plant.damage, level);
            return true;
        }
    }
    return false;
}
bool hypnoshroom_action(Level& level, Plant& plant){
    return false;
}
bool iceshroom_action(Level& level, Plant& plant){
    return false;
}
bool jalapeno_action(Level& level, Plant& plant){
    for (int col = 0; col < level.cols; col++){
        std::list<Zombie*> &cell = level.zombie_grid[plant.lane][col];
        while(!cell.empty()){
            cell.front()->get_damaged(plant.damage, level);
        }
    }
    plant.get_damaged(9999, level); // self destruct
    return true;
}
bool peashooter_action(Level& level, Plant& plant){
    for (int i = plant.col; i < level.cols; i++)
    {
        Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
        if (target_zombie == nullptr)
        {
            continue;
        }
        target_zombie->get_damaged(plant.damage, level);
        plant.frame_action_available = level.frame + plant.action_interval;
        return true;
    }
    return false;
}
bool potatomine_action(Level& level, Plant& plant){
    std::list<Zombie*> &cell = level.zombie_grid[plant.lane][plant.col];
    if(cell.empty()){
        return false;
    }
    while(!cell.empty()){
        cell.front()->get_damaged(plant.damage, level);
    }
    plant.get_damaged(9999, level); // self destruct
    return true;
}
bool puffshroom_action(Level& level, Plant& plant){
    return false;
}
bool repeaterpea_action(Level& level, Plant& plant){
    bool attacked = false;
    for (int shots = 0; shots <= 1; shots++){ // shoots twice
        for (int i = plant.col; i < level.cols; i++)
        {
            Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
            if (target_zombie == nullptr)
            {
                continue;
            }
            plant.frame_action_available = level.frame + plant.action_interval;
            target_zombie->get_damaged(plant.damage, level);
            attacked = true;
            break;
        }
    }
    return attacked;
}
bool scaredyshroom_action(Level& level, Plant& plant){
    return false;
}
bool snowpea_action(Level& level, Plant& plant){
    for (int i = plant.col; i < level.cols; i++)
    {
        Zombie *target_zombie = level.zombie_grid[plant.lane][i].front();
        if (target_zombie == nullptr)
        {
            continue;
        }
        target_zombie->get_damaged(plant.damage, level);
        // target_zombie->get_frozen(); !!!!
        plant.frame_action_available = level.frame + plant.action_interval;
        return true;
    }
    return false;
}
bool spikeweed_action(Level& level, Plant& plant){
    plant.frame_action_available = level.frame + plant.action_interval;
    std::list<Zombie*> &cell = level.zombie_grid[plant.lane][plant.col];
    if (cell.empty()){
        return false;
    }
    std::list<Zombie*>::iterator curr = cell.begin();
    std::list<Zombie*>::iterator backup = curr;
    while(curr != cell.end()){
        backup++;
        (*curr)->get_damaged(plant.damage, level);
        curr = backup;
    }
    return true;
}
bool squash_action(Level& level, Plant& plant){
    for (int pos_mod = 0; pos_mod <= 1; pos_mod++){
        if (plant.col + pos_mod >= level.cols){
            continue;
        }
        std::list<Zombie*> &cell = level.zombie_grid[plant.lane][plant.col + pos_mod];
        if(cell.empty()){
            // important! if you remove this, the plant will delete itself without damaging anything
            continue;
        }
        while(!cell.empty()){
            cell.back()->get_damaged(plant.damage, level);
        }
        plant.get_damaged(9999, level);
        return true;
    }
    return false;
}
bool sunflower_action(Level& level, Plant& plant){
    plant.frame_action_available = level.frame + plant.action_interval;
    level.suns += plant.damage;
    return true;
}
bool sunshroom_action(Level& level, Plant& plant){
    return false;
}
bool threepeater_action(Level& level, Plant& plant){
    bool attacked = false;
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
            plant.frame_action_available = level.frame + plant.action_interval;
            attacked = true;
            break;
        }
    }
    return attacked;
}
bool wallnut_action(Level& level, Plant& plant){
    return false;
}

