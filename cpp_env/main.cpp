#include "level.h"
#include <string>
using std::string;

std::deque<ZombieSpawnTemplate> get_level_data1() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate{second: 10, lane: 1, type: "normal"});
    level_data.push_back(ZombieSpawnTemplate{second: 20, lane: 3, type: "normal"});
    level_data.push_back(ZombieSpawnTemplate{second: 20, lane: 2, type: "buckethead"});
    return level_data;
}

std::deque<ZombieSpawnTemplate> get_level_data2() {
    std::deque<ZombieSpawnTemplate> level_data;
    level_data.push_back(ZombieSpawnTemplate{second: 10, lane: 1, type: "normal"});
    level_data.push_back(ZombieSpawnTemplate{second: 20, lane: 3, type: "normal"});
    level_data.push_back(ZombieSpawnTemplate{second: 20, lane: 2, type: "buckethead"});
    // level_data.push_back(ZombieSpawnTemplate{second: 50, lane: 1, type: "flag"});
    level_data.push_back(ZombieSpawnTemplate{second: 50, lane: 4, type: "newspaper"});
    // level_data.push_back(ZombieSpawnTemplate{second: 50, lane: 1, type: "conehead"});
    return level_data;
}

std::deque<Action> get_action_list1() {
    std::deque<Action> action_list;
    Action no_action = Action{plant_name: "no_action", lane: 0, col: 0};
    action_list.push_back(Action{plant_name: "sunflower", lane: 1, col: 0});
    action_list.push_back(Action{plant_name: "sunflower", lane: 1, col: 1});
    action_list.push_back(Action{plant_name: "peashooter", lane: 1, col: 2});
    action_list.push_back(Action{plant_name: "peashooter", lane: 1, col: 3});
    return action_list;
}

int main() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data1();
    // level_data.push_back(ZombieSpawnTemplate{second: 10, lane: 1, type: "normal"});
    // level_data.push_back(ZombieSpawnTemplate{second: 20, lane: 2, type: "buckethead"});
    // level_data.push_back(ZombieSpawnTemplate{second: 20, lane: 3, type: "normal"});
    // level_data.push_back(ZombieSpawnTemplate{second: 50, lane: 1, type: "flag"});
    // level_data.push_back(ZombieSpawnTemplate{second: 50, lane: 4, type: "newspaper"});
    // level_data.push_back(ZombieSpawnTemplate{second: 50, lane: 1, type: "conehead"});
    std::deque<Action> action_list = get_action_list1();
    Action no_action = Action{plant_name: "no_action", lane: 0, col: 0};
    // action_list.push_back(Action{plant_name: "sunflower", lane: 1, col: 0});
    // action_list.push_back(Action{plant_name: "sunflower", lane: 1, col: 1});
    // action_list.push_back(Action{plant_name: "peashooter", lane: 1, col: 2});
    // action_list.push_back(Action{plant_name: "peashooter", lane: 1, col: 3});

    //                lane, columns, fps, level_data
    Level env = Level(5,    10,      10, level_data);

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
