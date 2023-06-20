#include "cpp_env/level.hpp"
#include "cpp_mcts/mcts.h"
#include <chrono>

std::vector<int> default_chosen_plants = { CHERRYBOMB, CHOMPER, JALAPENO, PEASHOOTER, POTATOMINE, REPEATERPEA, SPIKEWEED, SQUASH, SUNFLOWER, THREEPEATER, WALLNUT};
std::vector<int> basic_chosen_plants = {PEASHOOTER, POTATOMINE, SQUASH, SUNFLOWER, WALLNUT};


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
    return level_data;
}
std::deque<ZombieSpawnTemplate> get_level_data4() {
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
    level_data.push_back(ZombieSpawnTemplate(110, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(111, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(112, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(120, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(120, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(150, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(150, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(150, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(185, 1, "normal"));
    return level_data;
}
std::deque<ZombieSpawnTemplate> get_level_data5() {
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
    level_data.push_back(ZombieSpawnTemplate(110, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(111, 1, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(112, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(120, 3, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(120, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(150, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(150, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(150, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(185, 1, "buckethead"));
    return level_data;
}
std::deque<ZombieSpawnTemplate> get_level_data6() {
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
    level_data.push_back(ZombieSpawnTemplate(110, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(111, 1, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(112, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(120, 3, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(120, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(150, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(150, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(150, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(185, 1, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(210, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(211, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(212, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(220, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(220, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(250, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(250, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(250, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(285, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(310, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(311, 1, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(312, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(320, 3, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(320, 2, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(350, 1, "flag"));
    level_data.push_back(ZombieSpawnTemplate(350, 4, "newspaper"));
    level_data.push_back(ZombieSpawnTemplate(350, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(385, 1, "buckethead"));
    return level_data;
}
void try_action(Level& level, Action action) {
    while (!level.is_action_legal(action)) {
        level.step();
    }
    std::cout << "[" << level.frame << "] " << "action taken: planted " << plant_data[action.plant_name].plant_name << " at: " << action.lane << ", " << action.col << std::endl;
    double winrate_percent = 100 * ((float)level.rollout(8, 10000, 1) / 10000);
    std::cout << "winrate before action: " << winrate_percent << "%" << std::endl;
    level.step(action);
    winrate_percent = 100 * ((float)level.rollout(8, 10000, 1) / 10000);
    std::cout << "winrate after action: " << winrate_percent << "%" << std::endl;
}

void estimate_speed(Level& level) {
    run(level, 5000, 1, true);
}
int main() {
    Level env = Level(5, 10, 10, get_level_data6(), default_chosen_plants);
    std::cout << env.rollout(-1, 100000, 1) << std::endl;
    // estimate_speed(env);
    // std::cout << env.rollout(-1, 20, 4) << std::endl;
    // while (!env.done) {
    //     Action run_result = run(env, 1700, 1, true, 30);
    //     while (!env.is_action_legal(run_result) && !(env.done)){
    //         env.step();
    //     }
    //     if (env.done) {
    //         break;
    //     }
    //     std::cout << "[" << env.frame << "] " << "action taken: planted " << plant_data[run_result.plant_name].plant_name << " at: " << run_result.lane << ", " << run_result.col << std::endl;
    //     std::pair<int, int> timed_rollout_res = env.timed_rollout(8, 300, 1);
    //     double winrate_percent = 100 * ((float)timed_rollout_res.second / timed_rollout_res.first);
    //     std::cout << "winrate before action: " << winrate_percent << "%" << std::endl;
    //     env.step(run_result);
    //     timed_rollout_res = env.timed_rollout(8, 300, 1);
    //     winrate_percent = 100 * ((float)timed_rollout_res.second / timed_rollout_res.first);
    //     std::cout << "winrate after action: " << winrate_percent << "%" << std::endl;
    // }
    // std::cout << "win status: " << env.win << std::endl;
}