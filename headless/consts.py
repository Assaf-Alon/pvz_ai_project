
OUT_OF_FIELD = (None, None)

# Automatically collect suns
AUTO_COLLECT = True

# Number of selected plants
NUM_OF_PLANTS = 10

# Might not be used in code
FAST_RECHARGE = 7.5
SLOW_RECHARGE = 30
VERY_SLOW_RECHARGE = 50

# JSON filepaths:
PLANT_STATS_FILE_PATH = "resources/plant_stats.json"
ZOMBIE_STATS_FILE_PATH = "resources/zombie_stats.json"

LOGS_TO_STDERR = False
LOG_FILE_NAME = "pvz.log"
# LOG_FORMAT = "[%(asctime)s] %(message)s"
LOG_FORMAT = "%(message)s"

TYPECHECK = False # avoid circular imports while allowing typechecks and autocompletes