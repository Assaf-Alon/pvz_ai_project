#ifndef _PVZ_GAMES
#define _PVZ_GAMES
#include "level.hpp"
#include <utility>

using std::pair;
typedef vector<pair<int, Action>> ActionVec;

std::deque<ZombieSpawnTemplate> get_level_data1() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate{.second = 10, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 3, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 2, .type = "buckethead"});
    return level_data;
}

std::deque<ZombieSpawnTemplate> get_level_data2() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate{.second = 10, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 11, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 12, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 3, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 2, .type = "buckethead"});
    // level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 1, .type = "flag"});
    level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 4, .type = "newspaper"});
    // level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 1, .type = "conehead"});
    return level_data;
}

std::deque<ZombieSpawnTemplate> get_level_data3() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate{.second = 10, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 11, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 12, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 3, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 20, .lane = 2, .type = "buckethead"});
    level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 1, .type = "flag"});
    level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 4, .type = "newspaper"});
    level_data.push_back(ZombieSpawnTemplate{.second = 50, .lane = 1, .type = "conehead"});
    level_data.push_back(ZombieSpawnTemplate{.second = 85, .lane = 1, .type = "normal"});
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
    std::vector<PlantName> chosen_plants = {SUNFLOWER, PEASHOOTER, POTATOMINE, SQUASH, SPIKEWEED, WALLNUT};


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

std::vector<PlantName> get_plants3() {
    // std::vector<PlantName> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    std::vector<PlantName> chosen_plants = { CHOMPER };
    return chosen_plants;
}

bool play_game_random() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data3();
    std::vector<PlantName> chosen_plants       = get_plants3();
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
    std::vector<PlantName> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
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
    // std::vector<PlantName> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    std::vector<PlantName> chosen_plants = { CHERRYBOMB };
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
    level_data.push_back(ZombieSpawnTemplate{.second = 15, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 60, .lane = 1, .type = "normal"});
    level_data.push_back(ZombieSpawnTemplate{.second = 95, .lane = 1, .type = "normal"});
    std::vector<PlantName> chosen_plants       = { CHOMPER };
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

#endif // _PVZ_GAMES