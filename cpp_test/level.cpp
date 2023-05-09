#include "level.h"
#include <assert.h>
#include <iostream>
#include <string>

using std::string;

using std::cout;
using std::endl;

Level::Level(int lanes, int columns, int fps){
    this->lanes;
    this->cols = cols;
    this->suns = 50;
    this->frame = 1;
    this->last_sun_generated = 1;
    this->zombie_in_home_col = false;
    this->done = false;
    this->win = false;
    this->lawnmowers = new bool[lanes];    
    Plant* plant_list_head = nullptr;
    Zombie* zombie_list_head = nullptr;
    this->zombies_to_spawn = vector<Zombie2Spawn>();
    this->zombies_to_spawn.push_back(Zombie2Spawn(100, 2));
    this->zombies_to_spawn.push_back(Zombie2Spawn(300, 2));
}

void Level::plant(int lane, int column, bool isSunflower) {
    if (isSunflower) {
        assert(this->suns >= 50);
        cout << "[" << this->frame << "] Planted sunflower at " << lane << column; 
        this->suns -= 50;
    }
    else {
        assert(this->suns >= 100);
        cout << "[" << this->frame << "] Planted peashooter at " << lane << column; 
        this->suns -= 100;
    }
    Plant* new_plant = new Plant(lane, column, isSunflower);
    if (this->plant_list_head == nullptr) {
        this->plant_list_head = new_plant;
        return;
    }
    new_plant->next = this->plant_list_head;
    this->plant_list_head->prev = new_plant;
    this->plant_list_head = new_plant;
    return;
}

bool Level::step(string plant_type, int lane, int col){
    if (lane >= this->lanes || col >= this->cols){
        return false;
    }
    // Do zombies actions
    Zombie* zombie = this->zombie_list_head;
    while (zombie != nullptr) {
        zombie->do_action(this);
    }

    // Do plants actions
    Plant* plant = this->plant_list_head;
    while (plant != nullptr) {
        plant->do_action(this);
    }

    // Spawn zombies
    while (!this->zombies_to_spawn.empty() && this->zombies_to_spawn.back().frame == this->frame) {
        Zombie2Spawn zombie_template = this->zombies_to_spawn.back();
        this->zombies_to_spawn.pop_back();
        Zombie* new_zombie = new Zombie(zombie_template.lane, 9, this); // TODO - column
        if (this->zombie_list_head == nullptr) {
            this->zombie_list_head = new_zombie;
        }
        else {
            this->zombie_list_head->prev = new_zombie;
            new_zombie->next = this->zombie_list_head;
            this->zombie_list_head = new_zombie;
        }
    }
    // Spawn suns
    if (this->frame - this->last_sun_generated >= 100) {
        assert(this->frame - this->last_sun_generated == 100);
        this->suns += 25;
        this->last_sun_generated = this->frame;
        cout << "[" << this->frame << "] Generated sun" << endl;
    }
    // do_player_action
    if (plant_type == "No") {
    }
    else if(plant_type == "Sunflower"){
        this->plant(lane, col, true);
    }
    else if (plant_type == "Peashooter"){
        this->plant(lane, col, false);
    }
    else {
        cout << "NO WAY ; BOTTOM TEXT" << endl;
        return false;
    }
    
    // Check done
    if (this->zombie_in_home_col == true){
        // Zombie is trying to enter the house
        this->zombie_in_home_col = false;
        for (int lane = 0; lane < this->lanes; lane++){ // this sucks without a grid
            bool lane_lawnmower_triggered = false;
            Zombie* zombie = this->zombie_list_head;
            while (zombie != nullptr) {
                if (zombie->data->lane == lane && zombie->data->entering_house == true){
                    lane_lawnmower_triggered = true;
                    break;
                }
            }
            if (lane_lawnmower_triggered == true){
                if (this->lawnmowers[lane] == false){
                    this->done = true;
                    this->win = false;
                    cout << "killed by zombie in lane: " << lane << endl;
                    return false;
                }
                Zombie* lawnmower_victim = this->zombie_list_head;
                while (lawnmower_victim != nullptr){
                    if (lawnmower_victim->data->lane == lane){
                        lawnmower_victim->get_damaged(9999, this);
                        lawnmower_victim = this->zombie_list_head;
                    }
                }
            }
        }
    }

    if (this->done == false){
        if (this->zombies_to_spawn.empty() == true && this->zombie_list_head == nullptr){
            this->done = true;
            this->win = true;
        }
    }

    (this->frame)++;
    // return self.construct_state()
    return true;
}

// ====================================================================
// ====================================================================
// ====================================================================


Zombie::Zombie(int lane, int column, Level* level){
    for (int i = 0; i < 1024; i++){
        Zombie_data* data = &(level->zombie_data_array)[i];
        if (data->alive == 0){
            this->data = data;
            data->attack_interval = 0;
            data->move_interval = 0;
            data->last_action = level->frame;
            data->col = column;
            data->lane = lane;
            data->hp = 181;
            data->damage = 0;
            data->entering_house = false;
            break;
        }
    }
    this->next = nullptr;
    this->prev = nullptr;
}
void Zombie::attack(Level* level){
    if((level->frame - this->data->last_action) < this->data->move_interval){
        return;
    }
    
    Plant* current_plant = level->plant_list_head;
    while (current_plant != nullptr){
        if (current_plant->data->col == this->data->col && current_plant->data->lane == this->data->lane){
            current_plant->get_damaged(this->data->damage, level);
            this->data->last_action = level->frame;
            return;
        }
        else {
            current_plant = current_plant->next;
        }
    }
}
void Zombie::move(Level* level){
    if ((level->frame - this->data->last_action) < this->data->attack_interval){
        return;
    }
    this->data->last_action = level->frame;
    if (this->data->col == 0){
        level->zombie_in_home_col = true;
    }
    else {
        this->data->col -= 1;
    }
}
void Zombie::do_action(Level* level){
    this->attack(level);
    this->move(level);
    
}
void Zombie::get_damaged(int damage, Level* level){
    this->data->hp -= damage;
    if (this->data->hp > 0){
        return;
    }
    this->data->alive = 0;
    Zombie* next = this->next;
    Zombie* prev = this->prev;

    if (next != nullptr) {
        if (prev != nullptr) {
            // prev me next
            prev->next = next;
            next->prev = prev;
        }
        else {
            // NULL me next
            next->prev = nullptr;
            level->zombie_list_head = next;
        }
    }
    else { // next is null
        if (prev != nullptr){
            // prev me null
            prev->next = next;
        }
        else {
            // list empty after removal
            level->zombie_list_head == nullptr;
        }
    }
}


// ====================================================================
// ====================================================================
// ====================================================================



Plant::Plant(int lane, int column) {
    this->prev = nullptr;
    this->next = nullptr;
    this->data = new Plant_data();
    this->data->lane = lane;
    this->data->col = column;
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


