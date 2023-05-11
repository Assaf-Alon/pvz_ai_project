#include "level.h"
#include <assert.h>
#include <iostream>
#include <string>
#include <sstream>
#include <list>

#ifndef DNDEBUG
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << endl;
#else
#define LOG_FRAME(frame, msg)
#endif

using std::string;

using std::cout;
using std::endl;

Level::Level(int lanes, int columns, int fps){
    lanes = lanes;
    cols = cols;
    suns = 50;
    frame = 1;
    last_sun_generated = 1;
    zombie_in_home_col = false;
    done = false;
    win = false;
    lawnmowers = new bool[lanes];
    for (int i = 0; i < lanes; i++){
        lawnmowers[i] = true;
    }
    zombie_list = std::list<Zombie*>();
    zombie_grid = new std::list<Zombie*>*[lanes];
    for (int i = 0; i < lanes; i++){
        zombie_grid[i] = new std::list<Zombie*>[cols];
    }
    plant_list = std::list<Plant*>();
    plant_grid = new Plant**[lanes];
    for (int i = 0; i < lanes; i++){
        plant_grid[i] = new Plant*[cols];
        for (int j = 0; j < columns; j++){
            plant_grid[i][j] = nullptr;
        }
    }
    zombies_to_spawn = vector<Zombie2Spawn>();
    zombies_to_spawn.push_back(Zombie2Spawn(100, 2));
    zombies_to_spawn.push_back(Zombie2Spawn(300, 2));
}

bool Level::is_action_legal(string plant_name, int lane, int col){
    if (this->done == true){
        return false;
    }
    if (plant_name == "no_action"){
        return true;
    }
    if (lane >= this->lanes || col >= this->cols) {
        return false;
    }
    if (this->plant_grid[lane][col] != nullptr) {
        return false;
    }
    if (plant_name != "sunflower" && plant_name != "peashooter"){
        return false;
    }
    if (plant_name == "sunflower" && this->suns < 50){
        return false;
    }
    if (plant_name == "peashooter" && this->suns < 100){
        return false;
    }
}

void Level::plant(int lane, int column, bool isSunflower) {
    Plant* new_plant = new Plant(lane, column, this->frame, isSunflower);
    this->plant_list.push_front(new_plant);
    this->plant_grid[lane][column] = new_plant;
}
void Level::do_zombie_actions(){
    for (Zombie* zombie : this->zombie_list){
        zombie->do_action(this);
    }
}
void Level::do_plant_actions(){
    for (Plant* plant : this->plant_list){
        plant->do_action(this);
    }
}
void Level::do_player_action(string plant_name, int lane, int col){
    if (this->is_action_legal(plant_name, lane, col) == false){
        LOG_FRAME(this->frame, "ILLEGAL ACTION");
        return;
    }
    if (plant_name == "sunflower") {
        this->plant(lane, col, true);
        std::stringstream log_msg;
        log_msg << "planted sunflower at lane " << lane << " col " << col;
        LOG_FRAME(this->frame, log_msg.str());
    }
    else if (plant_name == "peashooter"){
        this->plant(lane, col, false);
        std::stringstream log_msg;
        log_msg << "planted peashooter at lane " << lane << " col " << col;
        LOG_FRAME(this->frame, log_msg.str());
    }
    else if (plant_name == "no_action"){
        // do nothing
        LOG_FRAME(this->frame, "no action");
    }
}
void Level::spawn_zombies(){
    while (!this->zombies_to_spawn.empty() && this->zombies_to_spawn.back().frame == this->frame) {
        Zombie2Spawn zombie_template = this->zombies_to_spawn.back();
        this->zombies_to_spawn.pop_back();
        Zombie* new_zombie = new Zombie(zombie_template.lane, this->cols - 1, this); // TODO - column
        this->zombie_list.push_back(new_zombie);
        this->zombie_grid[new_zombie->lane][new_zombie->col].push_back(new_zombie);
    }
}
void Level::spawn_suns(){
    if (this->frame - this->last_sun_generated >= 100) {
        assert(this->frame - this->last_sun_generated == 100);
        this->suns += 25;
        this->last_sun_generated = this->frame;
        LOG_FRAME(this->frame, "generated sun");
    }
}
void Level::check_endgame(){
    if (this->zombie_in_home_col == true){
        bool kill_lane = false;
        this->zombie_in_home_col = false;
        for (int lane = 0; lane < this->lanes; lane++){ // for lane in lanes
            for (Zombie* zombie : this->zombie_grid[lane][0]){ // for zombie in lane's 0th col
                if (zombie->entering_house == true){
                    if (this->lawnmowers[lane] == true){
                        this->lawnmowers[lane] = false;
                        kill_lane = true; // lawnmower kills all zombles in the lane
                        break;
                    }
                    else{
                        // yer ded
                        this->done = true;
                        this->win = false;
                        return;
                    }
                }
            }
            for (int col = 0; col < this->cols; col++){
                while (this->zombie_grid[lane][col].empty() == false) {
                    this->zombie_grid[lane][col].front()->get_damaged(9999, this);
                }
            }
        }
        if (this->zombies_to_spawn.empty() && this->zombie_list.empty()){
            //no  more zombies to spawn and no more alive zombies left!
            this->done = true;
            this->win = true;
        }
    }
}
bool Level::step(string plant_type, int lane, int col){
    if (lane >= this->lanes || col >= this->cols){
        return false;
    }
    this->do_zombie_actions();
    this->do_plant_actions();
    this->remove_dead_objects();
    this->do_player_action(plant_type, lane, col);
    this->spawn_zombies();
    this->spawn_suns();
    this->check_endgame();
    (this->frame)++;
    // return self.construct_state()
    return true;
}

// ====================================================================
// ====================================================================
// ====================================================================


Zombie::Zombie(int lane, int column, Level* level){
    // TODO: Placeholder values!! updaate!!!!
    lane = lane;
    col = column;
    damage = 1;
    hp = 181;
    move_interval = 10;
    attack_interval = 10;
    last_action = level->frame;
}
void Zombie::attack(Level* level){
    if((level->frame - this->last_action) < this->move_interval){
        return;
    }
    Plant* target_plant = level->plant_grid[this->lane][this->col];
    if (target_plant == nullptr) {
        return;
    }
    this->last_action = level->frame;
    target_plant->get_damaged(this->damage, level);
}
void Zombie::move(Level* level){
    if ((level->frame - this->last_action) < this->attack_interval){
        return;
    }
    this->last_action = level->frame;
    if (this->col == 0){
        level->zombie_in_home_col = true;
        this->entering_house = true;
    }
    else {
        level->zombie_grid[this->lane][this->col].remove(this);
        this->col -= 1;
        level->zombie_grid[this->lane][this->col].push_front(this);
    }
}
void Zombie::do_action(Level* level){
    this->attack(level);
    this->move(level);
    
}
void Zombie::get_damaged(int damage, Level* level){
    this->hp -= damage;
    if (this->hp > 0){
        return;
    }
    this->alive = 0;
    // remove self from both global and cell lists
    level->zombie_list.remove(this);
    level->zombie_grid[this->lane][this->col].remove(this);
    delete this;
}


// ====================================================================
// ====================================================================
// ====================================================================



Plant::Plant(int lane, int column, int frame, bool isSunflower) {
    /*
    int lane;
    int col;
    int hp;
    int damage;
    int attack_interval;
    int sun_interval;
    int last_action;
    bool isSunflower;
    */
    lane = lane;
    col = column;
    hp = 1000;
    damage = 0;
    attack_interval = 5;
    sun_interval = 5;
    last_action = frame;
    isSunflower = isSunflower;
}

Plant::Plant(int lane, int column, bool isSunflower) {
    this->prev = nullptr;
    this->next = nullptr;
    this->data = new Plant_data();
    this->data->lane = lane;
    this->data->col = column;
    this->data->hp = 300;
    if (isSunflower) {
        this->data->attack_interval = 999999;
        this->data->sun_interval = 50;
    }
    else {
        this->data->damage = 20;
        this->data->attack_interval = 10;
    }
}

void Plant::attack(Level* level) {
    this->data->last_action = level->frame;
    // pea shoot goes burr
}
void Plant::generate_sun(Level* level) {
    level->suns += 25;
}
void Plant::do_action(Level* level) {
    if (level->frame - this->data->last_action < level->frame) {
        return;
    }
    if (this->isSunflower) {
        this->generate_sun(level);
    }
    else {
        this->attack(level);
    }
}
void Plant::get_damaged(int damage, Level* level) {
    (this->data)->hp -= damage;
    if ((this->data)->hp > 0) {
        return;
    }
    Plant* next = this->next;
    Plant* prev = this->prev;
    if (next != nullptr) {
        if (prev != nullptr) {
            // prev me next
            prev->next = next;
            next->prev = prev;
        }
        else {
            // NULL me next
            next->prev = nullptr;
            level->plant_list_head = next;
        }
    }
    else { // next is null
        if (prev != nullptr){
            // prev me null
            prev->next = next;
        }
        else {
            // list empty after removal
            level->plant_list_head == nullptr;
        }
    }
}


