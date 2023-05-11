#include "level.h"
#include <assert.h>
#include <iostream>
#include <string>
#include <sstream>
#include <list>

#ifndef NDEBUG
#define LOG_FRAME(frame, msg) std::cout << "[" << frame << "] " << msg << endl;
#else
#define LOG_FRAME(frame, msg)
#endif

using std::string;

using std::cout;
using std::endl;

Level::Level(int lanes, int columns, int fps): lanes(lanes), cols(columns), fps(fps)
{
    this->suns = 50;
    this->frame = 1;
    this->last_sun_generated = 1;
    this->zombie_in_home_col = false;
    this->done = false;
    this->win = false;
    this->lawnmowers = new bool[lanes];
    for (int i = 0; i < lanes; i++)
    {
        this->lawnmowers[i] = true;
    }
    this->zombie_list = std::list<Zombie *>();
    this->zombie_grid = new std::list<Zombie *> *[lanes];
    for (int i = 0; i < lanes; i++)
    {
        this->zombie_grid[i] = new std::list<Zombie *>[cols];
    }
    this->plant_list = std::list<Plant *>();
    this->plant_grid = new Plant **[lanes];
    for (int i = 0; i < lanes; i++)
    {
        this->plant_grid[i] = new Plant *[cols];
        for (int j = 0; j < columns; j++)
        {
            this->plant_grid[i][j] = nullptr;
        }
    }
    this->zombies_to_spawn = std::list<Zombie2Spawn>();
    this->zombies_to_spawn.push_back(Zombie2Spawn(100, 2));
    this->zombies_to_spawn.push_back(Zombie2Spawn(300, 2));
}

bool Level::is_action_legal(const string &plant_name, int lane, int col)
{
    if (this->done == true)
    {
        return false;
    }
    if (plant_name == "no_action")
    {
        return true;
    }
    if (lane >= this->lanes || col >= this->cols)
    {
        return false;
    }
    if (this->plant_grid[lane][col] != nullptr)
    {
        return false;
    }
    if (plant_name != "sunflower" && plant_name != "peashooter")
    {
        return false;
    }
    if (plant_name == "sunflower" && this->suns < 50)
    {
        return false;
    }
    if (plant_name == "peashooter" && this->suns < 100)
    {
        return false;
    }
    return true;
}

void Level::plant(int lane, int column, bool isSunflower)
{
    Plant *new_plant = new Plant(lane, column, this->frame, isSunflower);
    this->plant_list.push_front(new_plant);
    this->plant_grid[lane][column] = new_plant;
}
void Level::do_zombie_actions()
{
    for (Zombie *zombie : this->zombie_list)
    {
        zombie->do_action(this);
    }
}
void Level::do_plant_actions()
{
    for (Plant *plant : this->plant_list)
    {
        plant->do_action(this);
    }
}
void Level::do_player_action(const string &plant_name, int lane, int col)
{
    if (this->is_action_legal(plant_name, lane, col) == false)
    {
        LOG_FRAME(this->frame, "ILLEGAL ACTION");
        return;
    }
    if (plant_name == "sunflower")
    {
        this->plant(lane, col, true);
        std::stringstream log_msg;
        log_msg << "planted sunflower at lane " << lane << " col " << col;
        LOG_FRAME(this->frame, log_msg.str());
    }
    else if (plant_name == "peashooter")
    {
        this->plant(lane, col, false);
        std::stringstream log_msg;
        log_msg << "planted peashooter at lane " << lane << " col " << col;
        LOG_FRAME(this->frame, log_msg.str());
    }
    else if (plant_name == "no_action")
    {
        // do nothing
        LOG_FRAME(this->frame, "no action");
    }
}
void Level::spawn_zombies()
{
    if (this->zombies_to_spawn.empty()) {
        return;
    }
    if (this->zombies_to_spawn.front().frame == this->frame) {
        Zombie2Spawn zombie_template = this->zombies_to_spawn.front();
        this->zombies_to_spawn.pop_front();
        Zombie* new_zombie = new Zombie(zombie_template.lane, this->cols - 1, this);
        this->zombie_list.push_back(new_zombie);
        this->zombie_grid[new_zombie->lane][new_zombie->col].push_back(new_zombie);
        std::stringstream log_msg;
        log_msg << "Spawning zombie in " << new_zombie->lane << "," << new_zombie->col;
        LOG_FRAME(this->frame, log_msg.str());
    }
}
void Level::spawn_suns()
{
    if (this->frame - this->last_sun_generated >= 100)
    {
        assert(this->frame - this->last_sun_generated == 100);
        this->suns += 25;
        this->last_sun_generated = this->frame;
        LOG_FRAME(this->frame, "generated sun");
    }
}
void Level::check_endgame()
{
    if (this->zombie_in_home_col == true)
    {
        bool kill_lane = false;
        this->zombie_in_home_col = false;
        for (int lane = 0; lane < this->lanes; lane++)
        { // for lane in lanes
            for (Zombie *zombie : this->zombie_grid[lane][0])
            { // for zombie in lane's 0th col
                if (zombie->entering_house == true)
                {
                    if (this->lawnmowers[lane] == true)
                    {
                        this->lawnmowers[lane] = false;
                        kill_lane = true; // lawnmower kills all zombles in the lane
                        break;
                    }
                    else
                    {
                        // yer ded
                        std::stringstream log_msg;
                        log_msg << "Zombie at " << zombie->lane << "," << zombie->col << " killed ya";
                        LOG_FRAME(this->frame, log_msg.str());
                        this->done = true;
                        this->win = false;
                        return;
                    }
                }
            }
            if (kill_lane == true)
            {
                kill_lane = false;
                for (int col = 0; col < this->cols; col++)
                {
                    while (this->zombie_grid[lane][col].empty() == false)
                    {
                        this->zombie_grid[lane][col].front()->get_damaged(9999, this);
                    }
                }
            }
        }
        if (this->zombies_to_spawn.empty() && this->zombie_list.empty())
        {
            // no  more zombies to spawn and no more alive zombies left!
            this->done = true;
            this->win = true;
        }
    }
}
bool Level::step(const string &plant_type, int lane, int col)
{
    if (lane >= this->lanes || col >= this->cols)
    {
        return false;
    }
    LOG_FRAME(this->frame, "performing step");
    this->do_zombie_actions();
    this->do_plant_actions();
    this->do_player_action(plant_type, lane, col);
    this->spawn_zombies();
    this->spawn_suns();
    this->check_endgame();
    (this->frame)++;
    // return self.construct_state()
    return true;
}

Level::~Level(){
    LOG_FRAME(this->frame, "destructor called");
    printf("zombies left on field: %d\n", this->zombie_list.size());
    printf("zombies left to spawn: %d\n", this->zombies_to_spawn.size());
    while (this->plant_list.empty() == false){
        this->plant_list.front()->get_damaged(9999, this);
    }
    while (this->zombie_list.empty() == false){
        this->zombie_list.front()->get_damaged(9999, this);
    }
    for (int lane = 0; lane < this->lanes; lane++){
        delete[] this->zombie_grid[lane];
        delete[] this->plant_grid[lane];
    }
    delete[] this->zombie_grid;
    delete[] this->plant_grid;
    delete[] this->lawnmowers;
}

// ====================================================================
// ====================================================================
// ====================================================================

Zombie::Zombie(int lane, int column, Level *level) : lane(lane), col(column), last_action(level->frame)
{
    // TODO: Placeholder values!! updaate!!!!
}
void Zombie::attack(Level *level)
{
    if ((level->frame - this->last_action) < static_cast<int>(this->move_interval * level->fps))
    {
        return;
    }
    Plant *target_plant = level->plant_grid[this->lane][this->col];
    if (target_plant == nullptr)
    {
        return;
    }
    std::stringstream log_msg;
    log_msg << "zombie at " << this->lane << ", " << this->col << " attacked";
    LOG_FRAME(level->frame, log_msg.str());
    this->last_action = level->frame;
    target_plant->get_damaged(this->damage, level);
}
void Zombie::move(Level *level)
{
    if ((level->frame - this->last_action) < static_cast<int>(this->attack_interval * level->fps))
    {
        return;
    }
    this->last_action = level->frame;
    if (this->col == 0)
    {
        level->zombie_in_home_col = true;
        this->entering_house = true;
    }
    else
    {
        std::stringstream log_msg;
        log_msg << "zombie at " << this->lane << ", " << this->col << " moved";
        LOG_FRAME(level->frame, log_msg.str());
        level->zombie_grid[this->lane][this->col].remove(this);
        this->col -= 1;
        level->zombie_grid[this->lane][this->col].push_front(this);
    }
}
void Zombie::do_action(Level *level)
{
    this->attack(level);
    this->move(level);
}
void Zombie::get_damaged(int damage, Level *level)
{
    std::stringstream log_msg;
    log_msg << "Zombie at " << this->lane << "," << this->col << " sustained " << damage << " damage";
    LOG_FRAME(level->frame, log_msg.str());
    this->hp -= damage;
    if (this->hp <= 0)
    {
        // remove self from both global and cell lists
        level->zombie_list.remove(this);
        level->zombie_grid[this->lane][this->col].remove(this);
        delete this;
    }
}

// ====================================================================
// ====================================================================
// ====================================================================

Plant::Plant(int lane, int column, int frame, bool isSunflower) : lane(lane), col(column), last_action(frame), isSunflower(isSunflower)
{
    hp = 300;
    damage = 20;
    if (isSunflower)
    {
        action_interval = 50;
    }
    else
    {
        action_interval = 10;
    }
}
void Plant::attack(Level *level)
{
    this->last_action = level->frame;
    std::stringstream log_msg;
    log_msg << "plant at " << this->lane << ", " << this->col << " attacked [NOT REALLY]";
    LOG_FRAME(level->frame, log_msg.str());
    // pea shoot goes burr
}
void Plant::generate_sun(Level *level)
{
    level->suns += 25;
    this->last_action = level->frame;
    std::stringstream log_msg;
    log_msg << "plant at " << this->lane << ", " << this->col << " generated sun";
    LOG_FRAME(level->frame, log_msg.str());
}
void Plant::do_action(Level *level)
{
    if ((level->frame - this->last_action) < static_cast<int>(this->action_interval * level->fps))
    {
        return;
    }
    if (this->isSunflower)
    {
        this->generate_sun(level);
    }
    else
    {
        this->attack(level);
    }
}
void Plant::get_damaged(int damage, Level *level)
{
    std::stringstream log_msg;
    log_msg << "Plant at " << this->lane << "," << this->col << " sustained " << damage << " damage";
    LOG_FRAME(level->frame, log_msg.str());
    this->hp -= damage;
    if (this->hp <= 0)
    {
        level->plant_list.remove(this);
        level->plant_grid[this->lane][this->col] = nullptr;
        delete this;
    }
}
