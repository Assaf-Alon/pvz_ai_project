#include "level.h"
#include <string>
#include <iostream>
#include <thread>
#include <vector>
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
    Action no_action("no_action", 0,  0);
    action_list.push_back(Action("sunflower", 1,  0));
    action_list.push_back(Action("sunflower", 1,  1));
    action_list.push_back(Action("peashooter", 1,  2));
    action_list.push_back(Action("peashooter", 1,  4));
    return action_list;
}

void play_game1() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data1();
    std::deque<Action> action_list = get_action_list1();
    Action no_action = Action("no_action", 0,  0);

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
void play_game1_but_copy_midway() {
    
    int switch_frame = 100;
    std::deque<ZombieSpawnTemplate> level_data = get_level_data1();
    std::deque<Action> action_list = get_action_list1();
    Action no_action = Action("no_action", 0,  0);

    std::deque<Action> copied_action_list;
    //                lane, columns, fps, level_data
    Level env = Level(5,    10,      10, level_data);
    Level* copied_env;
    Level* active_env = &env;
    while (!active_env->done) {
        if (action_list.empty()) {
            active_env->step(no_action);
        }
        else {
            Action next_action = action_list.front();
            if (active_env->is_action_legal(next_action)) {
                active_env->step(next_action);
                action_list.pop_front();
            }
            else {
                active_env->step(no_action);
            }
        }
        if (active_env->frame == switch_frame) {
            copied_env = new Level(env);
            copied_action_list = action_list;

            active_env = copied_env;
        }
    }
    delete copied_env;
    std::cout << "!!! Playing from the original environment until the end" << std::endl;
    while (!env.done) {
        if (copied_action_list.empty()) {
            env.step(no_action);
        }
        else {
            Action next_action = copied_action_list.front();
            if (env.is_action_legal(next_action)) {
                env.step(next_action);
                copied_action_list.pop_front();
            }
            else {
                env.step(no_action);
            }
        }
        if (env.frame == switch_frame) {
            copied_env = new Level(env);
            active_env = copied_env;
        }
    }
}

bool play_game_random() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data2();
    Action no_action = Action("no_action", 0,  0);

    //                lane, columns, fps, level_data
    Level env = Level(5,    10,      10, level_data);

    while (!env.done) {
        Action next_action = env.get_random_action();
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
        }
        else {
            env.step(no_action);
        }
    }
    return env.win;
}

bool play_game_random_w_rollouts() {
    std::deque<ZombieSpawnTemplate> level_data = get_level_data3();
    Action no_action = Action("no_action", 0,  0);

    //                lane, columns, fps, level_data
    Level env = Level(5,    10,      10, level_data);

    while (!env.done) {
        if (env.frame % 100 == 0) {
            std::cout << "["<< env.frame << "] Rollout: " << env.rollout(8, 10000) << std::endl;
        }
        Action next_action = env.get_random_action();
        if (env.is_action_legal(next_action)) {
            env.step(next_action);
        }
        else {
            env.step(no_action);
        }
    }
    return env.win;
}




void play_random_games(int num_games=10000) {
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

int main() {
    // play_game1();
    // play_game_random();
    // play_game1_but_copy_midway();
    // play_random_games(1);
    play_game_random_w_rollouts();
}
