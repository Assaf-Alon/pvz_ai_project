#include "level.hpp"
#include "zombie.hpp"
#include "plant.hpp"
#include <algorithm>
using std::cout;
using std::endl;
using std::string;
using std::vector;
using std::list;

Level::Level(int lanes, int columns, int fps, std::deque<ZombieSpawnTemplate> level_data, vector<int> legal_plants, bool randomize) : \
    lanes(lanes), cols(columns), fps(fps), level_data(level_data), randomize(randomize)
{
    this->plant_grid = vector<vector<Plant*>>(lanes, vector<Plant*>(cols, nullptr));
    this->zombie_grid = vector<vector<list<Zombie*>>>(lanes, vector<list<Zombie*>>(cols, list<Zombie*>()));
    this->lawnmowers = vector<bool>(lanes, true);
    this->sun_interval = this->fps * this->sun_interval_seconds;
    this->chosen_plants = std::vector<int>(legal_plants);
    this->plant_cooldowns = std::vector<int>(NUM_PLANTS, 99999);
    for (auto plant_name : legal_plants){
        this->plant_cooldowns[plant_name] = 0;
    }
    this->free_spaces.reserve(lanes * cols * 2);
    for(int lane = 0; lane < lanes; lane++){
        for(int col = 0; col < cols; col++){
            this->free_spaces.push_back(Pos(lane, col));
        }
    }
    
    for(auto& zombie : this->level_data){
        zombie.frame = zombie.second * fps;
    }
    if (randomize){
        this->randomize_level_data();
    }
}

Level* Level::clone(int clone_mode) const{
    /*
    clone mode effects:
    -1: force deterministic
    0: keep same as original 
    1: force random
    defaults to 0.
    */
    Level* cloned = new Level(*this);
    switch (clone_mode){
        case -1:
            cloned->randomize = false;
        break;
        case 0:
            if (this->randomize){
                cloned->randomize_level_data();
            }
        break;
        case 1:
            cloned->randomize = true;
            cloned->randomize_level_data();
        break;
    }
    return cloned;
}

void Level::randomize_level_data(double varience) {
    // std::cout << "randomizing" << std::endl;
    for (auto& zombie : this->level_data) {
        zombie.frame = static_cast<int>(get_normal_sample(zombie.second * this->fps, varience * this->fps));
        zombie.effective_lane = get_random_number(std::max(zombie.lane - 1, 0), std::min(zombie.lane + 1, this->lanes - 1));
    }
    std::sort(this->level_data.begin(), this->level_data.end());
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
    this->randomize = other_level.randomize;

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
    // this->plant_data = vector<PlantData>(other_level.plant_data);
    this->plant_cooldowns = vector<int>(other_level.plant_cooldowns);

    // Copy free spaces
    this->free_spaces = vector<Pos>(other_level.free_spaces);

    // Copy chosen plants
    this->chosen_plants = vector<int>(other_level.chosen_plants);

    // if (this->randomize){
    //     this->randomize_level_data();
    // }
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
    if (this->plant_cooldowns[action.plant_name] > this->frame)
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
    const PlantData &planted_plant_data = plant_data[action.plant_name];
    new_plant = new Plant(action.lane, action.col, planted_plant_data, this->frame, this->fps);
    this->suns -= planted_plant_data.cost;
    this->plant_list.push_back(new_plant);
    this->plant_grid[action.lane][action.col] = new_plant;
    this->plant_cooldowns[action.plant_name] = this->frame + planted_plant_data.recharge_seconds * this->fps;
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
    while (!this->level_data.empty() && this->level_data.front().frame <= this->frame)
    {
        ZombieSpawnTemplate zombie_template = this->level_data.front();
        this->level_data.pop_front();
        Zombie *new_zombie = new Zombie(zombie_template.type, zombie_template.effective_lane, *this);
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
        if (this->randomize) {
            this->last_sun_generated = static_cast<int>(get_normal_sample(this->frame, this->fps));
        }
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

void Level::deferred_step(const Action& action){
    while (!this->is_action_legal(action) && !this->done){
        this->step();
    }
    if (this->done){
        return;
    }
    this->step(action);
}

Observation Level::get_observation() const{
    Observation obs = vector<vector<vector<int>>>(this->lanes, vector<vector<int>>(this->cols, vector<int>(3, 0)));    
    for (int lane = 0; lane < this->lanes; lane++){
        for (int col = 0; col < this->cols; col++){
            if (this->plant_grid[lane][col] != nullptr){
                Plant* plant = this->plant_grid[lane][col];
                int total_hp = plant_data[plant->plant_type].hp;
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

State Level::get_state() const{
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
    return (this->frame >= this->plant_cooldowns[plant]) && (this->suns >= plant_data[plant].cost);
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
    for(int idx = 1; idx < static_cast<int>(plant_data.size()); idx++){
        if (this->plant_cooldowns[idx] < this->frame && plant_data[idx].cost <= this->suns){
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
        break;
        case 4:
        while(!env.done){
            static const vector<Action> action_space = vector<Action>(env.get_action_space());
            int most_wins = 0;
            Action best_action = Action();
            // omp_set_num_threads(8);
            #pragma omp parallel for
            for(int i = 0; i < 22; i++){
                Action next_action = action_space[get_random_number(0, action_space.size())];
                Level* cloned = env.clone();
                cloned->deferred_step(next_action);
                int wins = 0;
                if (cloned->done){
                    wins = cloned->win;
                }
                else {
                    wins = cloned->rollout(-1, 20, 1);
                }
                #pragma omp critical
                {
                    if(wins > most_wins){
                        most_wins = wins;
                        best_action = next_action;
                    }
                }
            }
            env.deferred_step(best_action);
        }
        break;
    }
    return env.win;
}
bool play_random_heuristic_game(Level env, heuristic_function& func, int mode){
    switch (mode){
        case 1:
        while (!env.done){
            double best_h_score = 0;
            Action best_action = Action();
            #pragma omp parallel for
            for(int i = 0; i < 50; i++){
                Action next_action = env.get_random_action();
                Level* cloned = env.clone();
                cloned->step(next_action);
                double score = func(*cloned);
                #pragma omp critical
                if (score > best_h_score){
                    best_h_score = score;
                    best_action = next_action;
                }
            }
            env.step(best_action);
        }
        break;
        case 2:
        static const vector<Action> action_space = vector<Action>(env.get_action_space());
        while(!env.done){
            double best_h_score = 0;
            Action best_action = Action();
            #pragma omp parallel for
            for(int i = 0; i < 50; i++){
                Action next_action = action_space[get_random_number(0, action_space.size() - 1)];
                Level* cloned = env.clone();
                cloned->deferred_step(next_action);
                double score = func(*cloned);
                #pragma omp critical
                if (score > best_h_score){
                    best_h_score = score;
                    best_action = next_action;
                }
            }
            env.deferred_step(best_action);
        }
        break;
    }
    return env.win;
}

int Level::rollout(int num_cpu, int num_games, int mode) const {
    std::vector<bool> victories(num_games, false);
    switch (num_cpu){
        case 1:
        for (int i = 0; i < num_games; i++){
            victories[i] = play_random_game(*this, mode);
        }
        break;
        case -1:
        // omp_set_num_threads(8);
        omp_set_dynamic(1);
        #pragma omp parallel for shared(victories)
        for (int i = 0; i < num_games; i++){
            victories[i] = play_random_game(*this, mode);
        }
        break;
        default:
        omp_set_num_threads(num_cpu);
        #pragma omp parallel for shared(victories)
        for (int i = 0; i < num_games; i++){
            victories[i] = play_random_game(*this, mode);
        }
        break;
    }
    return std::count(victories.begin(), victories.end(), true);
}

// returns pair(rollouts, victories)
std::pair<int, int> Level::timed_rollout(int num_cpu, int time_limit_ms, int mode) const {
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


int Level::count_plant(PlantName plant) const{
    int count = 0;
    for (int i = 0; i < this->lanes; i++)
    {
        for (int j = 0; j < this->cols; j++)
        {
            if (this->plant_grid[i][j] != nullptr && (this->plant_grid[i][j])->plant_type == plant) {
                count++;
            }
        }
    }
    return count;
}

int Level::count_plant() const{
    int count = 0;
    for (int i = 0; i < this->lanes; i++)
    {
        for (int j = 0; j < this->cols; j++)
        {
            if (this->plant_grid[i][j] != nullptr) {
                count++;
            }
        }
    }
    return count;
}

int Level::count_lawnmowers() const{
    return std::count(this->lawnmowers.begin(), this->lawnmowers.end(), true);
}