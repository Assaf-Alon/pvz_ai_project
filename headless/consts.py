
OUT_OF_FIELD = (None, None)

# Automatically collect suns
AUTO_COLLECT = True

# Number of selected plants
NUM_OF_PLANTS = 10

# Might not be used in code
FAST_RECHARGE = 7.5
SLOW_RECHARGE = 30
VERY_SLOW_RECHARGE = 50

# Shall lawnmowers go until the end of the lane or just kill a single zombie
LAWNMOWERS_AS_BULLETS = True

# JSON filepaths:
PLANT_STATS_FILE_PATH = "resources/plant_stats.json"
ZOMBIE_STATS_FILE_PATH = "resources/zombie_stats.json"

# Logging stuff
LOG_DEBUG = 10
LOG_INFO = 20
LOG_WARNING = 30
LOG_ERROR = 40

LOG_LEVEL = LOG_DEBUG
LOGS_TO_STDERR = False
LOG_FILE_NAME = "pvz.log"
# LOG_FORMAT = "[%(asctime)s] %(message)s"
LOG_FORMAT = "%(message)s"

TYPECHECK = False # avoid circular imports while allowing typechecks and autocompletes

# Random level generation
difficulty = {
    "easy": {
        "spawn_interval_low": 2,
        "spawn_interval_high": 7,
        "zombie_types": ["Normal", "Conehead", "Buckethead", "Newspaper", "Flag"],
        "zombie_weights": [0.4, 0.2, 0.2, 0.1, 0.1],
        "num_of_zombies_low": 1,
        "num_of_zombies_high": 4,
        "waves": 5,
        "first_spawn_low": 3,
        "first_spawn_high": 10,
    },
    "medium": {
        "spawn_interval_low": 1,
        "spawn_interval_high": 5,
        "zombie_types": ["Normal", "Conehead", "Buckethead", "Newspaper", "Flag"],
        "zombie_weights": [0.4, 0.2, 0.2, 0.1, 0.1],
        "num_of_zombies_low": 2,
        "num_of_zombies_high": 5,
        "waves": 10,
        "first_spawn_low": 3,
        "first_spawn_high": 6,
    },
    "hard": {
        "spawn_interval_low": 1,
        "spawn_interval_high": 3,
        "zombie_types": ["Normal", "Conehead", "Buckethead", "Newspaper", "Flag"],
        "zombie_weights": [0.2, 0.25, 0.25, 0.2, 0.1],
        "num_of_zombies_low": 3,
        "num_of_zombies_high": 7,
        "waves": 20,
        "first_spawn_low": 0,
        "first_spawn_high": 4,
    },
    "insane": {
        "spawn_interval_low": 1,
        "spawn_interval_high": 3,
        "zombie_types": ["Normal", "Conehead", "Buckethead", "Newspaper", "Flag"],
        "zombie_weights": [0.1, 0.3, 0.3, 0.2, 0.1],
        "num_of_zombies_low": 4,
        "num_of_zombies_high": 10,
        "waves": 35,
        "first_spawn_low": 0,
        "first_spawn_high": 4,
    }
}

# Zombie-related consts

