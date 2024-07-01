
################################################################################################################################################
############################################# CONSTANTS SECTION #################################################################################

PUSH_3_DAYS = ["barbel_bench_press", "shoulders_presses","triceps", "chest_cable_crossover", "shoulders_dumble_lateral_raises", "triceps2"]

PULL_3_DAYS = ["pullups","bent_over_row","biceps","lat_pulldown","seated_row","biceps2"]

LEGS_DAY = ["squat", "romanina_deadlift", "bulgarian_split_squat", "calf_raise", "leg_extensions", "leg_curls"]

PUSH_4_DAYS = ["barbel_bench_press", "dips", "chest_cable_crossover", "dumbbell_bench_press", "chest_incline_fly", "machine_chest_press"]

PULL_4_DAYS = ["pullups", "bent_over_row", "single_arm_row", "lat_pulldown", "seated_row"]

ARMS_4_DAYS =  ["shoulders_presses", "triceps1", "biceps1", "shoulders_dumble_lateral_raises", "triceps2", "biceps2"]

CARDIO = ["Threadmill", "Bicycle"]

################################################################################################################################################

class workout_day :

    def __init__(self, number_of_days, type_of_exercise, list_of_exercise ) -> None:
        self.number_of_days = number_of_days
        self.type_of_exercise = type_of_exercise
        self.list_of_exercise = list_of_exercise


########################################################################
# Description: Function to create list of default exercises for 3/4/5 gym days
# Queries DB:
#   - insert_many: insert exercises in Default exercises table
# Parameters:
#    - default_exercises_table : collection -> object for Default exercises table
# Returns: no return
####################################################################
def create_default_exercises (default_exercises_table):
    list_exercises = list()
    list_exercises.append (workout_day (3, "push", PUSH_3_DAYS).__dict__)
    list_exercises.append (workout_day (3, "pull", PULL_3_DAYS).__dict__)
    list_exercises.append (workout_day (3, "legs", LEGS_DAY).__dict__)
    list_exercises.append (workout_day (4, "push", PUSH_4_DAYS).__dict__)
    list_exercises.append (workout_day (4, "pull", PULL_4_DAYS).__dict__)
    list_exercises.append (workout_day (4, "arms", ARMS_4_DAYS).__dict__)
    list_exercises.append (workout_day (4, "legs", LEGS_DAY).__dict__)
    list_exercises.append (workout_day (5, "cardio", CARDIO).__dict__)

    default_exercises_table.insert_many(list_exercises)

####################################################################
# This function was called only once to generate the default exercises table
# If developer wants to update table, this function has to be called again
####################################################################
# create_default_exercises(default_exercises_table=None)
