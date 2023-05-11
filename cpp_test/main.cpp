#include "level.h"
#include <string>
using std::string;
// #define NDEBUG
int main() {
    for (int i = 0; i < 1000; i++){
    //                lane, columns, fps
        Level env = Level(5,    10,      10);

        while (!env.done) {
            if (env.frame == 1) {
                env.step("sunflower", 0, 0);
            }
            if (env.frame == 105) {
                env.step("sunflower", 1, 0);
            }
            if (env.frame == 250) {
                env.step("peashooter", 2, 0);
            }
            else {
                env.step("no_action", -1, -1);
            }
        }
    }
}
