#include "level.h"
#include <string>
#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
using std::string;
#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif
#include <cstdlib>
#include <omp.h>

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
// void play_game1_but_copy_midway() {
    
//     int switch_frame = 100;
//     std::deque<ZombieSpawnTemplate> level_data = get_level_data1();
//     std::deque<Action> action_list = get_action_list1();
//     Action no_action = Action("no_action", 0,  0);

//     std::deque<Action> copied_action_list;
//     //                lane, columns, fps, level_data
//     Level env = Level(5,    10,      10, level_data);
//     Level* copied_env;
//     Level* active_env = &env;
//     while (!active_env->done) {
//         if (action_list.empty()) {
//             active_env->step(no_action);
//         }
//         else {
//             Action next_action = action_list.front();
//             if (active_env->is_action_legal(next_action)) {
//                 active_env->step(next_action);
//                 action_list.pop_front();
//             }
//             else {
//                 active_env->step(no_action);
//             }
//         }
//         if (active_env->frame == switch_frame) {
//             copied_env = new Level(env);
//             copied_action_list = action_list;

//             active_env = copied_env;
//         }
//     }
//     delete copied_env;
//     std::cout << "!!! Playing from the original environment until the end" << std::endl;
//     while (!env.done) {
//         if (copied_action_list.empty()) {
//             env.step(no_action);
//         }
//         else {
//             Action next_action = copied_action_list.front();
//             if (env.is_action_legal(next_action)) {
//                 env.step(next_action);
//                 copied_action_list.pop_front();
//             }
//             else {
//                 env.step(no_action);
//             }
//         }
//         if (env.frame == switch_frame) {
//             copied_env = new Level(env);
//             active_env = copied_env;
//         }
//     }
// }

bool play_game_random() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data3();
    Action no_action = Action(NO_PLANT, 0,  0);
    std::vector<PlantName> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};


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


void estimate_game_duration(int num_games){
    // std::vector<bool> victories(num_games, false);
    int wins = 0;
    omp_set_num_threads(8);
    auto start = std::chrono::high_resolution_clock::now();
    #pragma omp parallel for shared(wins)
    for(int i = 0; i < num_games; i++){
        wins += play_game_random();
    }
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    std::cout << "Time taken by function: " << ((float)duration.count() / num_games) / 1000000 << " secs" << std::endl;
    std::cout << "wins: " << wins << std::endl;
}

int main() {
    // play_game1();
    play_game_random();
    // play_game1_but_copy_midway();
    // play_random_games(10000);
    // play_game_random_w_rollouts(10000);
    // estimate_game_duration(1000000);
    // play_random_games(1);
}
