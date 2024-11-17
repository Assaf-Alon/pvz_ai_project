#include "game_engine/level.hpp"
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
std::deque<ZombieSpawnTemplate> get_level_data_9(){
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate(20, 0, "normal"));
    level_data.push_back(ZombieSpawnTemplate(50, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(70, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(90, 0, "normal"));
    level_data.push_back(ZombieSpawnTemplate(90, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(110, 4, "normal"));
    level_data.push_back(ZombieSpawnTemplate(110, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(130, 0, "pole"));
    level_data.push_back(ZombieSpawnTemplate(155, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(155, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(156, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(175, 4, "pole"));
    level_data.push_back(ZombieSpawnTemplate(175, 0, "normal"));
    level_data.push_back(ZombieSpawnTemplate(195, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(195, 4, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(215, 4, "flag"));
    level_data.push_back(ZombieSpawnTemplate(216, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(216, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(216, 2, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(216, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(216, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(217, 0, "normal"));
    level_data.push_back(ZombieSpawnTemplate(217, 0, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(220, 0, "pole"));
    level_data.push_back(ZombieSpawnTemplate(220, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(221, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(236, 3, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(260, 0, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(260, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(260, 4, "pole"));
    level_data.push_back(ZombieSpawnTemplate(270, 2, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(270, 0, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(270, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(285, 0, "normal"));
    level_data.push_back(ZombieSpawnTemplate(285, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(285, 4, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(300, 0, "normal"));
    level_data.push_back(ZombieSpawnTemplate(300, 1, "pole"));
    level_data.push_back(ZombieSpawnTemplate(300, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(301, 2, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(310, 3, "buckethead"));
    level_data.push_back(ZombieSpawnTemplate(310, 4, "normal"));
    level_data.push_back(ZombieSpawnTemplate(310, 4, "normal"));
    level_data.push_back(ZombieSpawnTemplate(322, 0, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(322, 1, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(322, 2, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(331, 1, "pole"));
    level_data.push_back(ZombieSpawnTemplate(331, 4, "normal"));
    level_data.push_back(ZombieSpawnTemplate(331, 3, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(332, 3, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(370, 0, "flag"));
    level_data.push_back(ZombieSpawnTemplate(371, 4, "pole"));
    level_data.push_back(ZombieSpawnTemplate(371, 3, "normal"));
    level_data.push_back(ZombieSpawnTemplate(371, 3, "conehead"));
    level_data.push_back(ZombieSpawnTemplate(371, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(372, 2, "normal"));
    level_data.push_back(ZombieSpawnTemplate(372, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(372, 1, "normal"));
    level_data.push_back(ZombieSpawnTemplate(372, 0, "normal"));
    level_data.push_back(ZombieSpawnTemplate(372, 0, "buckethead"));
    return level_data;

}
void try_action(Level& level, Action action) {
    while (!level.is_action_legal(action)) {
        level.step();
    }
    std::cout << "[" << level.frame << "] " << "action taken: planted " << plant_data[action.plant_name].plant_name << " at: " << action.lane << ", " << action.col << std::endl;
    double winrate_percent = 100 * ((float)level.rollout(10000, 1) / 10000);
    std::cout << "winrate before action: " << winrate_percent << "%" << std::endl;
    level.step(action);
    winrate_percent = 100 * ((float)level.rollout(10000, 1) / 10000);
    std::cout << "winrate after action: " << winrate_percent << "%" << std::endl;
}

void estimate_speed(Level& level) {
    run(level, 5000, 1, true, 1.4);
}
int main() {
    Level env = Level(5, 10, 10, get_level_data_9(), basic_chosen_plants);
    // std::cout << env.rollout(1, 100000, 1) << std::endl;
    // estimate_speed(env);
    // std::cout << env.rollout(-1, 20, 4) << std::endl;
    while (!env.done) {
        Action run_result = run(env, 4000, 8, true, 0.1, PARALLEL_TREES, HEURISTIC_SELECT, FULL_EXPAND, 0);
        while (!env.is_action_legal(run_result) && !(env.done)){
            env.step();
        }
        if (env.done) {
            break;
        }
        std::cout << "[" << env.frame << "] " << "action taken: planted " << plant_data[run_result.plant_name].plant_name << " at: " << run_result.lane << ", " << run_result.col << std::endl;
        std::pair<int, int> timed_rollout_res = env.timed_rollout(300, 1);
        double winrate_percent = 100 * ((float)timed_rollout_res.second / timed_rollout_res.first);
        std::cout << "winrate before action: " << winrate_percent << "%" << std::endl;
        env.step(run_result);
        timed_rollout_res = env.timed_rollout(300, 1);
        winrate_percent = 100 * ((float)timed_rollout_res.second / timed_rollout_res.first);
        std::cout << "winrate after action: " << winrate_percent << "%" << std::endl;
    }
    std::cout << "win status: " << env.win << std::endl;
}