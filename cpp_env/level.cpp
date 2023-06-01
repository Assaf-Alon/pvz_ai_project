#include "level.h"
using std::cout;
using std::endl;
using std::string;
using std::vector;
using std::list;
using std::unique_ptr;

std::random_device dev;
std::mt19937 rng(dev());

Level::Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate> &level_data, vector<PlantName> legal_plants) : lanes(lanes), cols(columns), fps(fps), level_data(level_data)
{
    this->plant_grid = vector<vector<Plant*>>(lanes, vector<Plant*>(cols, nullptr));
    this->zombie_grid = vector<vector<list<Zombie*>>>(lanes, vector<list<Zombie*>>(cols, list<Zombie*>()));
    this->lawnmowers = vector<bool>(lanes, true);
    this->sun_interval = this->fps * this->sun_interval_seconds;

    // std::random_device dev;
    // std::mt19937 rng(dev());
    // this->random_gen = rng;
    // make some of these constexprs!
    this->plant_data = std::vector<PlantData>(NUM_PLANTS, PlantData(this->fps, 0,0,0,0,0,PlantAction(&wallnut_action), "no_plant"));
    this->plant_data[SUNFLOWER] = PlantData(this->fps, 300, 25, 24.25, 7.5, 50, PlantAction(&sunflower_action), "sunflower");
    this->plant_data[PEASHOOTER] = PlantData(this->fps, 300, 20, 1.425, 7.5, 100, PlantAction(&peashooter_action), "peashooter");
    this->plant_data[POTATOMINE] = PlantData(this->fps, 300, 1800, 15, 30, 25, PlantAction(&potatomine_action), "potatomine");
    this->plant_data[WALLNUT] = PlantData(this->fps, 4000, 0, 9999, 30, 50, PlantAction(&wallnut_action), "wallnut");
    this->plant_data[SQUASH] = PlantData(this->fps, 300, 1800, 1.425, 30, 50, PlantAction(&squash_action), "squash");
    this->plant_data[SPIKEWEED] = PlantData(this->fps, 300, 20, 1, 7.5, 100, PlantAction(&spikeweed_action), "spikeweed");

    for (PlantName plant_name : legal_plants){
        plant_data[plant_name].next_available_frame = 0;
    }
}
Level::Level(const Level& other_level)
{
    this->lanes = other_level.lanes;
    this->cols = other_level.cols;
    this->suns = other_level.suns;
    this->frame = other_level.frame;
    this->last_sun_generated = other_level.last_sun_generated;
    this->sun_interval_seconds = other_level.sun_interval_seconds;
    this->zombie_in_home_col = other_level.zombie_in_home_col;
    this->done = other_level.done;
    this->win = other_level.win;
    this->sun_interval = other_level.sun_interval;
    this->fps = other_level.fps;
    this->return_state = other_level.return_state;

    // Generate new rng
    // std::random_device dev;
    // std::mt19937 rng(dev());
    // this->random_gen = rng;

    // Copy lawnmowers
    this->lawnmowers = other_level.lawnmowers;

    // Copy zombies
    this->zombie_grid = vector<vector<list<Zombie*>>>(lanes, vector<list<Zombie*>>(this->cols, list<Zombie*>()));
    for (int lane = 0; lane < lanes; lane++){
        for (int col = 0; col < cols; col++){
            for (Zombie* zombie : other_level.zombie_grid[lane][col]){
                Zombie* zombie_copy = new Zombie(*zombie);
                this->zombie_grid[lane][col].push_back(zombie_copy);
                this->zombie_list.push_back(zombie_copy);
            }
        }
    }

    // Copy plants
    this->plant_grid = vector<vector<Plant*>>(this->lanes, vector<Plant*>(this->cols, nullptr));
    for (int lane = 0; lane < lanes; lane++) {
        for (int col = 0; col < cols; col++) {
            if (other_level.plant_grid[lane][col] == nullptr){
                continue;
            }
            Plant* new_plant = other_level.plant_grid[lane][col]->clone();
            this->plant_grid[lane][col] = new_plant;
            this->plant_list.push_back(new_plant);
        }
    }

    // Copy level data
    this->level_data = std::deque<ZombieSpawnTemplate>(other_level.level_data);

    // Copy cooldown
    this->plant_data = vector<PlantData>(other_level.plant_data);
}

bool Level::is_action_legal(const Action &action) const
{
    if (action.plant_name == NO_PLANT)
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
    if (this->plant_data[action.plant_name].next_available_frame > this->frame)
    {
        return false;
    }
    if (plant_data[action.plant_name].cost > this->suns)
    {
        return false;
    }
    if (this->done == true)
    {
        return false;
    }
    return true;
}

void Level::plant(const Action &action)
{
    Plant *new_plant = nullptr;
    PlantData &planted_plant_data = this->plant_data[action.plant_name];
    new_plant = new Plant(action.lane, action.col, planted_plant_data, this->frame, this->fps);
    this->suns -= planted_plant_data.cost;
    this->plant_list.push_back(new_plant);
    this->plant_grid[action.lane][action.col] = new_plant;
    planted_plant_data.next_available_frame = this->frame + planted_plant_data.recharge_seconds * this->fps;
}
void Level::do_zombie_actions()
{
    for (Zombie* zombie : this->zombie_list)
    {
        zombie->do_action(*this);
    }
}
void Level::do_plant_actions()
{
    // Note! this may cause issues with exploading plants and the iterator being invalidated!!!!
    // note, it does!
    // std::list<Plant*> tmp_list = std::list<Plant*>(this->plant_list);
    // for(Plant* plant : tmp_list){
    //     plant->do_action(*this);
    // }
    std::list<Plant*>::iterator curr = this->plant_list.begin();
    std::list<Plant*>::iterator backup = curr;
    while(curr != this->plant_list.end()){
        backup++;
        (*curr)->do_action(*this);
        curr = backup;
    }

}
void Level::do_player_action(const Action &action)
{
    if (this->is_action_legal(action) == false)
    {
        LOG_FRAME(this->frame, "ILLEGAL ACTION");
        return;
    }
    if (action.plant_name == NO_PLANT)
    {
        // do nothing
        // LOG_FRAME(this->frame, "no action");
        return;
    }

    this->plant(action);
    #ifdef DEBUG
    std::stringstream log_msg;
    log_msg << "Planted " << this->plant_data[action.plant_name].plant_name << " at lane " << action.lane << " col " << action.col;
    LOG_FRAME(this->frame, log_msg.str());
    LOG_FRAME(this->frame, " >> Plants left: " + std::to_string(this->plant_list.size()));
    #endif
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
        log_msg << "Spawning zombie in " << new_zombie->lane << ", " << new_zombie->col;
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
        #ifdef DEBUG
        LOG_FRAME(this->frame, "Generated sun. total: " + std::to_string(this->suns));
        #endif
    }
}
bool Level::check_endgame()
{
    if (this->zombie_in_home_col == false) // TODO - Why do we check this here?
    {
        if (this->level_data.empty() && this->zombie_list.empty())
        {
            // no  more zombies to spawn and no more alive zombies left!
            this->done = true;
            this->win = true;
            return true;
        }
        // no zombies at home, and there're still zombies alive / to spawn
        return false;
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
                    log_msg << "Zombie at " << zombie->lane << ", " << zombie->col << " killed ya";
                    LOG_FRAME(this->frame, log_msg.str());
                    #endif
                    this->done = true;
                    this->win = false;
                    return true;
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
            if (this->level_data.empty() && this->zombie_list.empty())
            {
                // no  more zombies to spawn and no more alive zombies left!
                this->done = true;
                this->win = true;
                return true;
            }
        }
    }
    return false;
}
State *Level::step(const Action &action)
{
    if (!this->is_action_legal(action)){
        return nullptr;
    }
    // LOG_FRAME(this->frame, "performing step");
    #ifdef DEBUG
    if (frame % 100 == 0) {
        std::stringstream log_msg;
        log_msg << "Zombies left to spawn: " << this->level_data.size();
        LOG_FRAME(this->frame, log_msg.str());
    }
    #endif
    this->do_zombie_actions();
    this->do_plant_actions();
    this->do_player_action(action);
    this->spawn_zombies();
    this->spawn_suns();
    if (this->check_endgame()) {
        #ifdef DEBUG
        std::stringstream log_msg;
        if (this->win) {
            log_msg << "You've won!";
        }
        else {
            log_msg << "You've lost!";
        }
        LOG_FRAME(this->frame, log_msg.str());
        #endif
        return nullptr;
    }
    (this->frame)++;
    if (this->return_state == true)
    {
        // return self.construct_state()
    }
    return nullptr;
}

int Level::get_random_uniform(int min, int max) const {
    std::uniform_int_distribution<std::mt19937::result_type> dist(min, max); // distribution in range [min, max]
    return dist(rng);
}

// TODO - get suns as input?
PlantName Level::get_random_plant() const {
    #ifdef DEBUG
    LOG_FRAME(frame, "Randomizing plant");
    #endif
    vector<PlantName> legal_plants;
    for(int idx = 1; idx < static_cast<int>(this->plant_data.size()); idx++){
        if (this->plant_data[idx].next_available_frame < this->frame){
            legal_plants.push_back(static_cast<PlantName>(idx));
        }
    }
    if(legal_plants.empty()){
        return NO_PLANT;
    }
    int plant = get_random_uniform(0, legal_plants.size() - 1);
    return legal_plants[plant];
}

    // As long as a substantial amount of the board is free, this should work efficiently
bool Level::get_random_position(int& lane, int& col) const {
    for (int attempt = 0; attempt < 3; attempt++) {
        lane = get_random_uniform(0, lanes - 1);
        col = get_random_uniform(0, cols - 1);
        if (this->plant_grid[lane][col] == nullptr) {
            return true;
        }
    }
    lane = -1;
    col = -1;
    return false; // no_action
}

// TODO - discuss optimizing this
const Action Level::get_random_action() const {
    if (this->suns < 50) { // this->suns < this->cheapest_plant_cost?
        return this->no_action;
    }
    if (get_random_uniform(1,10) <= 4) { // 40% chance to do nothing, consider some other probability
        return this->no_action;
    }
    int lane, col;
    if (!get_random_position(lane, col)){
        return this->no_action;
    }
    for (int i = 0; i < 5; i++) { // 5 attempts to plant a plant
        PlantName plant_name = get_random_plant();
        if(plant_name == NO_PLANT){
            continue;
        }
        Action action(plant_name, lane, col);
        if (this->is_action_legal(action)) {
            return action;
        }
    }
    return no_action;
}

Level::~Level()
{
    #ifdef DEBUG
    LOG_FRAME(this->frame, "destructor called");
    std::cout << "Zombies left on field: " << this->zombie_list.size() << std::endl;
    std::cout << "Zombies left to spawn: " << this->level_data.size() << std::endl;
    #endif
    while (this->plant_list.empty() == false)
    {
        this->plant_list.front()->get_damaged(9999, *this);
    }
    while (this->zombie_list.empty() == false)
    {
        this->zombie_list.front()->get_damaged(9999, *this);
    }
    // for (int lane = 0; lane < this->lanes; lane++)
    // {
    //     delete[] this->zombie_grid[lane];
    //     delete[] this->plant_grid[lane];
    // }
    // delete[] this->zombie_grid;
    // delete[] this->plant_grid;
    // delete[] this->lawnmowers;
}

bool Level::play_random_game(Level env) {
    Action no_action = Action(NO_PLANT, 0,  0);
    while (!env.done) {
        Action next_action = env.get_random_action();
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
        }
        else {
            env.step(no_action);
        }
    }
    return env.win;
}

int Level::rollout(int num_cpu, int num_games) {
    std::vector<bool> victories(num_games, false);
    omp_set_num_threads(num_cpu);
    #pragma omp parallel for shared(victories)
    for (int i = 0; i < num_games; i++){
        victories[i] = Level::play_random_game(*this);
        // victories[i] = play_random_game(*this);
    }
    
    return std::count(victories.begin(), victories.end(), true);
}

// Level::Level() : lanes(5), cols(10), fps(10), level_data(std::deque<ZombieSpawnTemplate>()) {}
