#include "level.h"
#include <string>
using std::string;
int main() {
    //                lane, columns, fps
    Level env = Level(5,    10,      10);

    while (!env.done) {
        if (env.frame == 1) {
            env.step("Sunflower", 0, 0);
        }
        if (env.frame == 105) {
            env.step("Sunflower", 1, 0);
        }
        if (env.frame == 250) {
            env.step("Peashooter", 2, 0);
        }
        else {
            env.step("No", -1, -1);
        }
    }
}
