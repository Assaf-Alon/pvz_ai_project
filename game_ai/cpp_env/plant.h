#ifndef _PVZ_PLANT
#define _PVZ_PLANT
#include <string>
#include <functional>

class Level;
// typedef std::function<bool(Level&, Plant&)> PlantAction;
class Action;
class PlantInfo;

class PlantData;
/*
class PlantData {
    public:
    int hp;
    int damage;
    float action_interval_seconds;
    int action_interval;
    float recharge_seconds;
    int recharge;
    int cost;
    std::function<bool(Level&, Plant&)> action_func;
    std::string plant_name;
    int next_available_frame = 9999;
    int plant_type;
    PlantData() = default;
    PlantData(int fps, int hp, int damage, float action_interval_seconds, float recharge_seconds, int cost, std::function<bool(Level&, Plant&)> action_func, std::string plant_name, int plant_type) : \
    hp(hp), damage(damage), action_interval_seconds(action_interval_seconds), recharge_seconds(recharge_seconds), cost(cost), action_func(action_func), plant_name(plant_name), plant_type(plant_type) {
        this->action_interval = static_cast<int>(action_interval_seconds * fps);
        this->recharge = static_cast<int>(recharge_seconds * fps);
    };
};
*/

class Plant {
public:
    int lane;
    int col;
    int hp;
    int cost;
    int damage; // for sun-generating plants, this is the value of the sun generated
    // float action_interval_seconds;
    int action_interval;
    // float recharge_seconds;
    int recharge;
    int frame_action_available;
    int fps;   // for clone...?
    int plant_type;
    std::string plant_name;
    Plant(int lane, int column, const PlantData &plant_data, int frame, int fps);
    std::function<bool(Level&, Plant&)> action;
    PlantInfo get_info();
    void do_action(Level& level);
    void get_damaged(int damage, Level& level);
    Plant* clone() const;
    ~Plant() = default;
};

bool cherrybomb_action(Level& level, Plant& plant);
bool chomper_action(Level& level, Plant& plant);
bool hypnoshroom_action(Level& level, Plant& plant);
bool iceshroom_action(Level& level, Plant& plant);
bool jalapeno_action(Level& level, Plant& plant);
bool peashooter_action(Level& level, Plant& plant);
bool potatomine_action(Level& level, Plant& plant);
bool puffshroom_action(Level& level, Plant& plant);
bool repeaterpea_action(Level& level, Plant& plant);
bool scaredyshroom_action(Level& level, Plant& plant);
bool snowpea_action(Level& level, Plant& plant);
bool spikeweed_action(Level& level, Plant& plant);
bool squash_action(Level& level, Plant& plant);
bool sunflower_action(Level& level, Plant& plant);
bool sunshroom_action(Level& level, Plant& plant);
bool threepeater_action(Level& level, Plant& plant);
bool wallnut_action(Level& level, Plant& plant);

#endif