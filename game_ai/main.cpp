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
}
