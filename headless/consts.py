
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