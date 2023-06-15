#include "level.hpp"
#include "zombie.h"
#include "plant.h"
using std::cout;
using std::endl;
using std::string;
using std::vector;
using std::list;
using std::unique_ptr;

// std::random_device dev;
// std::mt19937 rng(dev());
// thread_local std::mt19937 rng(std::random_device{}());
// std::minstd_rand rng(std::random_device{}());
// std::ranlux48 rng(std::random_device{}());

inline int get_random_number(const int min, const int max){ 
    thread_local std::mt19937 generator(std::random_device{}());
    std::uniform_int_distribution<int> distribution(min, max);
    return distribution(generator);
}

Level::Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate> level_data, vector<int> legal_plants) : lanes(lanes), cols(columns), fps(fps), level_data(level_data)
{
    this->plant_grid = vector<vector<Plant*>>(lanes, vector<Plant*>(cols, nullptr));
    this->zombie_grid = vector<vector<list<Zombie*>>>(lanes, vector<list<Zombie*>>(cols, list<Zombie*>()));
    this->lawnmowers = vector<bool>(lanes, true);
    this->sun_interval = this->fps * this->sun_interval_seconds;

    // make some of these constexprs!
    this->plant_data = std::vector<PlantData>(NUM_PLANTS, PlantData(this->fps, 0,0,0,0,0,PlantAction(&wallnut_action), "no_plant", NO_PLANT));
    
    this->plant_data[CHERRYBOMB]    = PlantData(this->fps, 5000, 9000, 1.2,   50,  150, PlantAction(&cherrybomb_action), "cherrybomb", CHERRYBOMB);
    this->plant_data[CHOMPER]       = PlantData(this->fps, 300,  9000, 42,    7.5, 150, PlantAction(&chomper_action), "chomper", CHOMPER);
    this->plant_data[HYPNOSHROOM]   = PlantData(this->fps, 300,  20,   0,     30,  75,  PlantAction(&hypnoshroom_action), "hypnoshroom", HYPNOSHROOM);
    this->plant_data[ICESHROOM]     = PlantData(this->fps, 5000, 20,   1,     50,  75,  PlantAction(&iceshroom_action), "iceshroom", ICESHROOM);
    this->plant_data[JALAPENO]      = PlantData(this->fps, 300,  9000, 1,     50,  125, PlantAction(&jalapeno_action), "jalapeno", JALAPENO);
    this->plant_data[PEASHOOTER]    = PlantData(this->fps, 300,  20,   1.425, 7.5, 100, PlantAction(&peashooter_action), "peashooter", PEASHOOTER);
    this->plant_data[POTATOMINE]    = PlantData(this->fps, 300,  1800, 15,    30,  25,  PlantAction(&potatomine_action), "potatomine", POTATOMINE);
    this->plant_data[PUFFSHROOM]    = PlantData(this->fps, 300,  20,   1.425, 7.5, 0,   PlantAction(&puffshroom_action), "puffshroom", PUFFSHROOM);
    this->plant_data[REPEATERPEA]   = PlantData(this->fps, 300,  20,   1.425, 7.5, 200, PlantAction(&repeaterpea_action), "repeaterpea", REPEATERPEA);
    this->plant_data[SCAREDYSHROOM] = PlantData(this->fps, 300,  20,   1.425, 7.5, 20,  PlantAction(&scaredyshroom_action), "scaredyshroom", SCAREDYSHROOM);
    this->plant_data[SNOWPEA]       = PlantData(this->fps, 300,  20,   1.425, 7.5, 175, PlantAction(&snowpea_action), "snowpea", SNOWPEA);
    this->plant_data[SPIKEWEED]     = PlantData(this->fps, 300,  20,   1,     7.5, 100, PlantAction(&spikeweed_action), "spikeweed", SPIKEWEED);
    this->plant_data[SQUASH]        = PlantData(this->fps, 300,  1800, 1.425, 30,  50,  PlantAction(&squash_action), "squash", SQUASH);
    this->plant_data[SUNFLOWER]     = PlantData(this->fps, 300,  25,   24.25, 7.5, 50,  PlantAction(&sunflower_action), "sunflower", SUNFLOWER);
    this->plant_data[SUNSHROOM]     = PlantData(this->fps, 300,  15,   24.25, 7.5, 25,  PlantAction(&sunshroom_action), "sunshroom", SUNSHROOM);
    this->plant_data[THREEPEATER]   = PlantData(this->fps, 300,  20,   1.425, 7.5, 325, PlantAction(&threepeater_action), "threepeater", THREEPEATER);
    this->plant_data[WALLNUT]       = PlantData(this->fps, 4000, 0,    9999,  30,  50,  PlantAction(&wallnut_action), "wallnut", WALLNUT);

    this->chosen_plants = std::vector<int>(legal_plants);
    for (auto plant_name : legal_plants){
        plant_data[plant_name].next_available_frame = 0;
    }
    this->free_spaces.reserve(lanes * cols * 2);
    for(int lane = 0; lane < lanes; lane++){
        for(int col = 0; col < cols; col++){
            this->free_spaces.push_back(Pos(lane, col));
        }
    }
}

Level* Level::clone() {
    return new Level(*this);
}

void Level::append_zombie(int second, int lane, std::string type){
    this->level_data.push_back(ZombieSpawnTemplate(second, lane, type));
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

    // Copy free spaces
    this->free_spaces = vector<Pos>(other_level.free_spaces);

    // Copy chosen plants
    this->chosen_plants = vector<int>(other_level.chosen_plants);
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

bool Level::is_action_legal(int plant, int row, int col) const
{
    return this->is_action_legal(Action((PlantName)plant, row, col));
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
    std::vector<Pos>& free_spaces = this->free_spaces;
    for (auto it = free_spaces.begin(); it != free_spaces.end(); it++){
        if (it->first == action.lane && it->second == action.col){
            free_spaces.erase(it);
            break;
        }
    }
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
void Level::step(const Action &action)
{
    if (!this->is_action_legal(action)){
        return;
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
        return;
    }
    (this->frame)++;
    if (this->return_state == true)
    {
        // return self.construct_state()
    }
}

void Level::step(int plant, int row, int col)
{
    this->step(Action(PlantName(plant), row, col));
}

Observation Level::get_observation(){
    Observation obs = vector<vector<vector<int>>>(this->lanes, vector<vector<int>>(this->cols, vector<int>(3, 0)));    
    for (int lane = 0; lane < this->lanes; lane++){
        for (int col = 0; col < this->cols; col++){
            if (this->plant_grid[lane][col] != nullptr){
                Plant* plant = this->plant_grid[lane][col];
                int total_hp = this->plant_data[plant->plant_type].hp;
                int hp_third = 1 + (int)((plant->hp - 1) / (int)(total_hp / 3));
                obs[lane][col][0] = plant->plant_type;
                obs[lane][col][1] = hp_third;
            }
            int danger_level = 0;
            int total_cell_hp = 0;
            for (auto zombie : this->zombie_grid[lane][col]){
                total_cell_hp += zombie->hp;
            }
            if (total_cell_hp == 0){
                danger_level = 0;
            }
            else {
                danger_level = 1 + total_cell_hp / 200;
            }
            obs[lane][col][2] = danger_level;
        }
    }
    return obs;
}

State Level::get_state(){
    PlantInfo empty_plant;
    empty_plant.plant_name = "no_plant";
    empty_plant.hp = 0;
    empty_plant.col = -1;
    empty_plant.lane = -1;
    State state;
    for (int lane = 0; lane < this->lanes; lane++){
        std::vector<Cell> lane_vector;
        for (int col = 0; col < this->cols; col++){
            Cell cell = Cell();
            if (this->plant_grid[lane][col]){
                cell.plant_info = this->plant_grid[lane][col]->get_info();
            }
            else {
                cell.plant_info = empty_plant;
            }
            for (Zombie* zombie : this->zombie_grid[lane][col]){
                cell.zombie_info_vec.push_back(zombie->get_info());
            }
            lane_vector.push_back(cell);
        }
        state.push_back(lane_vector);
    }
    return state;
}

int Level::get_random_plant() const {
    return this->chosen_plants[get_random_number(0, this->chosen_plants.size() - 1)];
}

bool Level::is_plantable(int plant) const {
    if (plant >= NUM_PLANTS || plant < NO_PLANT) {
        return false;
    }
    return (this->frame >= this->plant_data[plant].next_available_frame) && (this->suns >= this->plant_data[plant].cost);
}

void Level::step() {
    this->step(this->no_action);
}
// TODO - get suns as input?
PlantName Level::get_random_legal_plant() const {
    #ifdef DEBUG
    LOG_FRAME(frame, "Randomizing plant");
    #endif
    vector<PlantName> legal_plants;
    for(int idx = 1; idx < static_cast<int>(this->plant_data.size()); idx++){
        if (this->plant_data[idx].next_available_frame < this->frame && this->plant_data[idx].cost <= this->suns){
            legal_plants.push_back(static_cast<PlantName>(idx));
        }
    }
    if(legal_plants.empty()){
        #ifdef DEBUG
        LOG_FRAME(frame, " >> No legal plant");
        #endif
        return NO_PLANT;
    }
    int plant = get_random_number(0, legal_plants.size() - 1);
    return legal_plants[plant];
}

vector<Pos>* Level::get_all_legal_positions() {
    return &(this->free_spaces);
}

vector<Action> Level::get_action_space() const
{
    std::cout << "Generating action space" << std::endl;
    vector<Action> action_space;
    action_space.reserve(this->lanes * this->cols * this->chosen_plants.size() * 2);
    for (size_t plant_idx = 0; plant_idx < this->chosen_plants.size(); plant_idx++) {
        PlantName plant = (PlantName)this->chosen_plants[plant_idx];
        for (int lane = 0; lane < this->lanes; lane++) {
            for (int col = 0; col < this->cols; col++) {
                action_space.push_back(Action(plant, lane, col));
            }
        }
    }
    return action_space;
}

// guranteed to be a legal position if one exists
bool Level::get_random_position(int& lane, int& col) const {
    const vector<Pos>& free_spaces = this->free_spaces;
    if (free_spaces.size() == 0){
        lane = -1;
        col = -1;
        return false;
    }
    pair<int, int> position = free_spaces[get_random_number(0, free_spaces.size() - 1)];
    lane = position.first;
    col = position.second;
    return true;
}

// TODO - discuss optimizing this
const Action Level::get_random_action() const {
    if (this->suns < 50) { // this->suns < this->cheapest_plant_cost?
        return this->no_action;
    }
    if (get_random_number(1,10) <= 4) { // 40% chance to do nothing, consider some other probability
        return this->no_action;
    }
    int lane, col;
    if (!get_random_position(lane, col)){
        return this->no_action;
    }
    PlantName plant_name = get_random_legal_plant();
    return Action(plant_name, lane, col);
}

Level::~Level()
{
    #ifdef DEBUG
    LOG_FRAME(this->frame, "destructor called");
    std::cout << "Zombies left on field: " << this->zombie_list.size() << std::endl;
    std::cout << "Zombies left to spawn: " << this->level_data.size() << std::endl;
    #endif
    // while (this->plant_list.empty() == false)
    // {
    //     this->plant_list.front()->get_damaged(9999, *this);
    // }
    // while (this->zombie_list.empty() == false)
    // {
    //     this->zombie_list.front()->get_damaged(9999, *this);
    // }
    for (auto plant : this->plant_list) {
        delete plant;
    }
    for (auto zombie : this->zombie_list) {
        delete zombie;
    }
}

bool play_random_game(Level env, int randomization_mode){
    switch(randomization_mode){
        case 1: // for each step, choose a random action available right now
        while (!env.done) {
            env.step(env.get_random_action());
        }
        return env.win;
        break;
        case 2: // select next action, do empty steps until its possible, then do it
        while(!env.done) {
            int lane = get_random_number(0, env.lanes - 1);
            int col = get_random_number(0, env.cols - 1);
            int plant = env.get_random_plant();
            Action next_step = Action((PlantName)plant, lane, col);
            while (!env.is_action_legal(next_step) && !env.done){
                env.step();
            }
            if (env.done) {
                return env.win;
            }
            env.step(next_step);
        }
        break;
        case 3: // select next plant to plant, wait until it's possible, select random empty cell and plant it
        while(!env.done) {
            int next_plant = env.get_random_plant();
            while(!env.is_plantable(next_plant) && !env.done) {
                env.step();
            }
            if (env.done) {
                return env.win;
            }
            int lane, col;
            while(!env.get_random_position(lane, col) && !env.done) {
                env.step();
            }
            if (env.done) {
                return env.win;
            }
            env.step((PlantName)next_plant, lane, col);
        }
    }
    return env.win;
}

int Level::rollout(int num_cpu, int num_games, int mode) {
    std::vector<bool> victories(num_games, false);
    omp_set_num_threads(num_cpu);
    #pragma omp parallel for shared(victories)
    for (int i = 0; i < num_games; i++){
        victories[i] = play_random_game(*this, mode);
    }
    return std::count(victories.begin(), victories.end(), true);
}

// returns pair(rollouts, victories)
std::pair<int, int> Level::timed_rollout(int num_cpu, int time_limit_ms, int mode) {
    int rollouts = 0, victories = 0;
    auto start_time = std::chrono::high_resolution_clock::now();
    auto end_time = start_time + std::chrono::milliseconds(time_limit_ms);
    omp_set_num_threads(num_cpu);
    #pragma omp parallel reduction(+:victories) reduction(+:rollouts)
    while(std::chrono::high_resolution_clock::now() < end_time) {
        int win = play_random_game(*this, mode);
        victories += win;
        rollouts++;
    }
    return std::pair<int, int>(rollouts, victories);
}
