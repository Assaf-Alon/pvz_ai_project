// #include "level.hpp"
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
#include "games.hpp"

#define MICROSECONDS_IN_SECOND 1000000

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
//     while (!env.done) {level_data = get_level_data3();
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
    std::cout << "Time taken by function: " << ((float)duration.count() / num_games) / MICROSECONDS_IN_SECOND << " secs" << std::endl;
    std::cout << "wins: " << wins << std::endl;
}


int main() {
    // play_game1();
    // play_game_random();
    // play_game1_but_copy_midway();
    // play_random_games(10000);
    // play_game_random_w_rollouts(10000);
    auto level_data = get_level_data3();
    std::vector<int> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    Level level = Level(5,    10,      10, level_data,  chosen_plants);
    int timeout = 2000;
    int num_cpu = 8;
    std::pair<int, int> result = level.timed_rollout(num_cpu, timeout, 1);
    std::cout << "rollouts done: " << result.first << ", victories: " << result.second << std::endl;
    std::cout << "win proportion: " << (static_cast<double>(result.second) / result.first) * 100 << "%" << std::endl;
    std::cout << "time per rollout: " << static_cast<double>(timeout / 1000) / result.first << std::endl;
    result = level.timed_rollout(num_cpu, timeout, 2);
    std::cout << "rollouts done: " << result.first << ", victories: " << result.second << std::endl;
    std::cout << "win proportion: " << (static_cast<double>(result.second) / result.first) * 100 << "%" << std::endl;
    std::cout << "time per rollout: " << static_cast<double>(timeout / 1000) / result.first << std::endl;
    result = level.timed_rollout(num_cpu, timeout, 3);
    std::cout << "rollouts done: " << result.first << ", victories: " << result.second << std::endl;
    std::cout << "win proportion: " << (static_cast<double>(result.second) / result.first) * 100 << "%" << std::endl;
    std::cout << "time per rollout: " << static_cast<double>(timeout / 1000) / result.first << std::endl;
    // play_game_random_w_rollouts_after_action(10000);
    // estimate_game_duration(100000);
    // play_random_games(1);
    // play_game_single_plant(CHERRYBOMB);
    // play_specific_game();
    // std::vector<int> chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
    // auto level_data = get_level_data3();
    // Level level = Level(5,    10,      10, level_data,  chosen_plants);
    // int wins = level.rollout(8,1);
    // std::cout << wins << std::endl;
}
