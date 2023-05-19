#include "level.h"



using std::cout;
using std::endl;
using std::string;

Level::Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate> &level_data) : lanes(lanes), cols(columns), fps(fps), level_data(level_data)
{
    this->sun_interval = this->fps * this->sun_interval_seconds;
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
}
Level::Level(const Level &other_level)
{
}

bool Level::is_action_legal(const Action &action)
{
    if (this->done == true)
    {
        return false;
    }
    if (action.plant_name == "no_action")
    {
        return true;
    }
    if (action.lane >= this->lanes || action.col >= this->cols || action.lane < 0 || action.col < 0)
    {
        return false;
    }
    if (this->plant_grid[action.lane][action.col] != nullptr)
    {
        return false;
    }
    if (action.plant_name != "sunflower" && action.plant_name != "peashooter")
    {
        return false;
    }
    if (action.plant_name == "sunflower" && this->suns < 50)
    {
        return false;
    }
    if (action.plant_name == "peashooter" && this->suns < 100)
    {
        return false;
    }
    return true;
}

void Level::plant(const Action &action)
{
    // TODO: fix up this selector
    Plant *new_plant = nullptr;
    if (action.plant_name == "sunflower")
    {
        new_plant = new Sunflower(action.lane, action.col, this->frame, this->fps);
        this->suns -= new_plant->cost;
    }
    else if (action.plant_name == "peashooter")
    {
        new_plant = new Peashooter(action.lane, action.col, this->frame, this->fps);
        this->suns -= new_plant->cost;
    }
    this->plant_list.push_front(new_plant);
    this->plant_grid[action.lane][action.col] = new_plant;
}
void Level::do_zombie_actions()
{
    for (Zombie *zombie : this->zombie_list)
    {
        zombie->do_action(*this);
    }
}
void Level::do_plant_actions()
{
    for (Plant *plant : this->plant_list)
    {
        plant->do_action(*this);
    }
}
void Level::do_player_action(const Action &action)
{
    if (this->is_action_legal(action) == false)
    {
        LOG_FRAME(this->frame, "ILLEGAL ACTION");
        return;
    }
    if (action.plant_name == "no_action")
    {
        // do nothing
        LOG_FRAME(this->frame, "no action");
    }
    else
    {
        this->plant(action);
#ifdef DEBUG
        std::stringstream log_msg;
        log_msg << "planted " << action.plant_name << " at lane " << action.lane << " col " << action.col;
        LOG_FRAME(this->frame, log_msg.str());
#endif
    }
}
void Level::spawn_zombies()
{
    while (!this->level_data.empty() && this->level_data.front().second * this->fps <= this->frame)
    {
        ZombieSpawnTemplate zombie_template = this->level_data.front();
        this->level_data.pop_front();
        Zombie *new_zombie = new Zombie(zombie_template.type, zombie_template.lane, *this);
        this->zombie_list.push_back(new_zombie);
        this->zombie_grid[new_zombie->lane][new_zombie->col].push_back(new_zombie);
#ifdef DEBUG
        std::stringstream log_msg;
        log_msg << "Spawning zombie in " << new_zombie->lane << "," << new_zombie->col;
        LOG_FRAME(this->frame, log_msg.str());
#endif
    }
}
void Level::spawn_suns()
{
    if ((this->frame - this->last_sun_generated) >= this->sun_interval)
    {
        this->suns += 25;
        this->last_sun_generated = this->frame;
        LOG_FRAME(this->frame, "generated sun");
    }
}
void Level::check_endgame()
{
    if (this->zombie_in_home_col == false)
    {
        if (this->level_data.empty() && this->zombie_list.empty())
        {
            // no  more zombies to spawn and no more alive zombies left!
            this->done = true;
            this->win = true;
        }
        return;
    }
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
#ifdef DEBUG
                    std::stringstream log_msg;
                    log_msg << "Zombie at " << zombie->lane << "," << zombie->col << " killed ya";
                    LOG_FRAME(this->frame, log_msg.str());
#endif
                    this->done = true;
                    this->win = false;
                    return;
                }
            }
        }
        if (kill_lane == true)
        {
        // consider optimizing by iterating over main list with iterators instead
        // this way, we iterate once over the big list in o(n) and then for each cell, call erase()
        // total complexity bounded by o(2n)
            #ifdef DEBUG
            std::stringstream log_msg;
            log_msg << "lawnmower destroying lane number " << lane;
            LOG_FRAME(this->frame, log_msg.str());
            #endif
            kill_lane = false;
            for (int col = 0; col < this->cols; col++)
            {
                while (this->zombie_grid[lane][col].empty() == false)
                {
                    this->zombie_grid[lane][col].front()->get_damaged(9999, *this);
                }
            }
        }
    } 
}
State *Level::step(const Action &action)
{
    if (!this->is_action_legal(action)){
        return nullptr;
    }
    LOG_FRAME(this->frame, "performing step");
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "zombies left to spawn: " << this->level_data.size();
    LOG_FRAME(this->frame, log_msg.str());
    #endif
    this->do_zombie_actions();
    this->do_plant_actions();
    this->do_player_action(action);
    this->spawn_zombies();
    this->spawn_suns();
    this->check_endgame();
    if (this->done) {
        std::stringstream log_msg;
        if (this->win) {
            log_msg << "You've won!";
        }
        else {
            log_msg << "You've lost!";
        }
        LOG_FRAME(this->frame, log_msg.str());
        return nullptr;
    }

    (this->frame)++;
    if (this->return_state == true)
    {
        // return self.construct_state()
    }
    return nullptr;
}

// Action& Level::get_random_action(){
// }

Level::~Level()
{
    LOG_FRAME(this->frame, "destructor called");
    std::cout << "zombies left on field: " << this->zombie_list.size() << std::endl;
    std::cout << "zombies left to spawn: " << this->level_data.size() << std::endl;
    while (this->plant_list.empty() == false)
    {
        this->plant_list.front()->get_damaged(9999, *this);
    }
    while (this->zombie_list.empty() == false)
    {
        this->zombie_list.front()->get_damaged(9999, *this);
    }
    for (int lane = 0; lane < this->lanes; lane++)
    {
        delete[] this->zombie_grid[lane];
        delete[] this->plant_grid[lane];
    }
    delete[] this->zombie_grid;
    delete[] this->plant_grid;
    delete[] this->lawnmowers;
}
