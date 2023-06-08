#ifndef _PVZ_GAMES
#define _PVZ_GAMES
#include "level.hpp"
#include <utility>
#include <stdlib.h>
#include <unistd.h>

using std::pair;
typedef vector<pair<int, Action>> ActionVec;

std::vector<int> default_chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};


std::deque<ZombieSpawnTemplate> get_level_data1() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    return level_data;
}

std::deque<ZombieSpawnTemplate> get_level_data2() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(11, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(12, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    // level_data.push_back(ZombieSpawnTemplate(50, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(50, 4, "newspaper"));
    // level_data.push_back(ZombieSpawnTemplate(50, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(11, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(12, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    // level_data.push_back(ZombieSpawnTemplate(50, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(50, 4, "newspaper"));
    // level_data.push_back(ZombieSpawnTemplate(50, 1, "conehead"));
    return level_data;
}

std::deque<ZombieSpawnTemplate> get_level_data3() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(11, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(12, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(50, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(85, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(10, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(11, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(12, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(20, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(50, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(50, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(85, 1, "normal"));
    return level_data;
}

std::deque<Action> get_action_list1() {
    std::deque<Action> action_list;
    Action no_action(NO_PLANT, 0,  0);
    action_list.push_back(Action(SUNFLOWER, 1,  0));
    action_list.push_back(Action(SUNFLOWER, 1,  1));
    action_list.push_back(Action(PEASHOOTER, 1,  2));
    action_list.push_back(Action(PEASHOOTER, 1,  4));
    return action_list;
}

void play_game1() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data1();
    std::deque<Action> action_list = get_action_list1();
    Action no_action = Action(NO_PLANT, 0,  0);
    std::vector<int> chosen_plants = {SUNFLOWER, PEASHOOTER, POTATOMINE, SQUASH, SPIKEWEED, WALLNUT};
    std::vector<int> chosen_plants = {SUNFLOWER, PEASHOOTER, POTATOMINE, SQUASH, SPIKEWEED, WALLNUT};


    //                lane, columns, fps, level_data
    Level env = Level(5,    10,      10, level_data,  chosen_plants);


    while (!env.done) {
        if (action_list.empty()) {
            env.step(no_action);
        }
        else {
            Action next_action = action_list.front();
            if (env.is_action_legal(next_action)) {
                env.step(next_action);
                action_list.pop_front();
            }
            else {
                env.step(no_action);
            }
        }
    }
}

std::vector<int> get_plants3() {
    std::vector<int> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    // std::vector<int> chosen_plants = { CHOMPER };
    return chosen_plants;
}

bool play_game_random() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data3();
    std::vector<int> chosen_plants       = get_plants3();
    std::vector<int> chosen_plants       = get_plants3();
    Action no_action = Action(NO_PLANT, 0,  0);

    //                lane, columns, fps, level_data
    Level env = Level(5,    10,      10, level_data, chosen_plants);

    while (!env.done) {
        Action next_action = env.get_random_action();
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
        }
        else {
            std::cout << "illegal move!" << std::endl;
            env.step(no_action);
        }
    }
    return env.win;
}

bool play_game_random_w_rollouts(int rollotus_per_cycle) {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data3();
    Action no_action = Action(NO_PLANT, 0,  0);
    std::vector<int> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    std::vector<int> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    //                lane, columns, fps, level_data, legal_plants
    Level env = Level(5,    10,      10, level_data,  chosen_plants);
    int num_rollouts = 0;
    while (!env.done) {
        if (env.frame % 100 == 0) {
            std::cout << "["<< env.frame << "] Rollout: " << env.rollout(8, rollotus_per_cycle) << std::endl;
            num_rollouts += rollotus_per_cycle;
        }
        Action next_action = env.get_random_action();
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
        }
        else {
            env.step(no_action);
        }
    }
    std::cout << "number of rollouts: " << num_rollouts << std::endl;
    return env.win;
}

bool play_game_random_w_rollouts_after_action(int rollotus_per_cycle) {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data3();
    Action no_action = Action(NO_PLANT, 0,  0);
    // std::vector<int> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    std::vector<int> chosen_plants = { CHERRYBOMB };
    // std::vector<int> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    std::vector<int> chosen_plants = { CHERRYBOMB };
    //                lane, columns, fps, level_data, legal_plants
    Level env = Level(5,    10,      10, level_data,  chosen_plants);
    ActionVec actions_taken = ActionVec();
    int num_rollouts = 0;
    while (!env.done) {
        
        Action next_action = env.get_random_action();
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
            if (next_action.plant_name != NO_PLANT) {
                std::cout << "["<< env.frame << "] Rollout wins: " << env.rollout(8, rollotus_per_cycle) << " / " << rollotus_per_cycle << std::endl;
                num_rollouts += rollotus_per_cycle;
                actions_taken.push_back(pair<int, Action>(env.frame, next_action));
            }
            continue;
        }
        env.step(no_action);
    }
    std::cout << "number of rollouts: " << num_rollouts << std::endl;
    std::cout << "Won? " << env.win << std::endl;
    std::cout << "Actions taken: " << std::endl;
    for (auto p : actions_taken) {
        std::cout << "[" << p.first << "] Plant: " << env.plant_data[p.second.plant_name].plant_name << ", Lane: " << p.second.lane << ", Col: " << p.second.col << std::endl;
    }
    return env.win;
}



void play_random_games(int num_games) {
    std::vector<bool> victories(num_games, false);
    omp_set_num_threads(8);
    #pragma omp parallel for shared(victories)
    for (int i = 0; i < num_games; i++){
        victories[i] = play_game_random();
    }
    for (auto game : victories){
        std::cout << game;
    }
    std::cout << std::endl;
}

bool play_specific_game() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate(15, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(60, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(95, 1, "normal"));
    std::vector<int> chosen_plants       = { CHOMPER };
    level_data.push_back(ZombieSpawnTemplate(15, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(60, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(95, 1, "normal"));
    std::vector<int> chosen_plants       = { CHOMPER };
    Action no_action = Action(NO_PLANT, 0,  0);

    //                lane, columns, fps, level_data
    Level env = Level(5,    10,      10, level_data, chosen_plants);
    env.suns = 500;
    while (!env.done) {
        Action next_action = Action(CHOMPER, 1, 5);
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
        }
        else {
            env.step(no_action);
        }
    }
    return env.win;
}


void play_game_with_state_printing(){
    // Action no_action = Action(NO_PLANT, 0,  0);
    Level env(5, 10, 10, get_level_data3(), default_chosen_plants);
    while(!env.done){
        if (env.frame % 10 == 0){
            std::cout << "frame: " << env.frame << std::endl;
            State state = env.get_state();
            for (auto lane : state) {
                for (auto cell : lane) {
                    auto plant_info = cell.plant_info;
                    std::cout << " | " << plant_info.plant_name << ", hp: " << plant_info.hp << " | ";
                    for (auto zomb : cell.zombie_info_vec) {
                        std::cout << " | " << zomb.type << ", hp: " << zomb.hp << " | ";
                    }
                }
                std::cout << std::endl;
            }
        }
        Action next_action = env.get_random_action();
        env.step(next_action);
    }
}
void play_game_with_observations(){
    const std::string yellow = "\033[43m";
    const std::string red =    "\033[41m";
    const std::string green =  "\033[42m";
    const std::string blue =   "\033[44m";
    const std::string reset =  "\033[0m";
    Level env(5, 10, 10, get_level_data3(), default_chosen_plants);
    std::string linebreak = "";
    for (int cols = 0; cols < env.cols; cols++) linebreak += "_______";
    while(!env.done){
        auto obs = env.get_observation();
        std::system("clear");
        std::cout << "Frame number: " << env.frame << ", zombies on field: " << env.zombie_list.size() << std::endl;
        std::cout << linebreak << std::endl;
        for (int lane = 0; lane < env.lanes; lane++){
            for (int col = 0; col < env.cols; col++){
                CellObservation cell = obs[lane][col];
                std::string plant_color;
                switch (cell.plant_hp_phase){
                    case 0: plant_color = red;
                    break;
                    case 1: plant_color = yellow;
                    break;
                    case 2: plant_color = green;
                    break;
                    default: plant_color = reset;
                }
                if (cell.plant_type == 0) plant_color = reset;
                std::cout << "|" << plant_color << cell.plant_type << reset << "," << cell.plant_hp_phase << ",";
                std::string zomb_color;
                switch (cell.zombie_danger_level) {
                    case 0: zomb_color = reset;
                    break;
                    case 1: zomb_color = yellow;
                    break;
                    case 2: zomb_color = red;
                    break;
                    default: zomb_color = red;
                    break;
                }
                std::cout << zomb_color << cell.zombie_danger_level << reset << "|"; 
            }
            std::cout << std::endl;
        }
        // std::cout << std::endl;
        env.step(env.get_random_action());
        usleep(50000);
    }
}

#endif // _PVZ_GAMES