

class Exercises :

    def __init__(self, email, date, type_of_exercise, weight, sets, repetitions) -> None:
        self.email = email
        self.date = date
        self.type_of_exercise = type_of_exercise
        self.weight = weight
        self.sets = sets
        self.repetitions = repetitions

def introduce_one_exercise (db) :

    username_exercises = db.get_collection("Exercises")

    email = input("Please introduce your email : ")
    date = input ("Introduce the date when you exercises : ")
    type_of_exercise = input ("What types of exercises have you performed? : ")
    sets = input ("How many sets have you done? : ")
    weight = input ("What weight have you used for each set? :")
    repetitions = input ("How many repetitions have you done? : ")

    username_exercises.insert_one({"Exercises":{
                            "email": email, 
                            "Date" : date,
                            "Type_of_exercise" : type_of_exercise,
                            "sets" : sets ,
                            "weight" : weight,
                            "repetition" : repetitions
                    }})

    ex = Exercises (email, date, type_of_exercise, weight, sets, repetitions)

    print ("Exercitiile au fost adaugate ")
    return ex

# introduce_one_exercise(get_db())

def introduce_more_exercises (db) :

    username_exercises = db.get_collection("Exercises")

    email = input("email : ")
    date = input ("Introduce the date when you exercises : ")
    type_of_exercise = input ("What types of exercises have you performed? : ")
    sets = input ("How many sets have you done? : ")
    weight = input ("What weight have you used for each set? :")
    repetitions = input ("How many repetitions have you done? : ")

    username_exercises.insert_many({"Exercises":{
                            "email": email, 
                            "Date" : date,
                            "Type_of_exercise" : type_of_exercise,
                            "sets" : sets ,
                            "weight" : weight,
                            "repetition" : repetitions
                    }})

    ex = Exercises (email, date, type_of_exercise, weight, sets, repetitions)

    print ("Exercitiile au fost adaugate ")
    return ex

# introduce_more_exercises(get_db())

class workout_day :

    def __init__(self, number_of_days, type_of_exercise, list_of_exercise ) -> None:
        
        self.number_of_days = number_of_days
        self.type_of_exercise = type_of_exercise
        self.list_of_exercise = list_of_exercise

def create_default_exercises (default_exercises_table):
    list_exercises = list()
    list_exercises.append (workout_day (3, "push", push_data_base_3_days).__dict__)
    list_exercises.append (workout_day (3, "pull", pull_data_base_3_days).__dict__)
    list_exercises.append (workout_day (3, "legs", legs_day).__dict__)
    list_exercises.append (workout_day (4, "push", push_4_days).__dict__)
    list_exercises.append (workout_day (4, "pull", pull_4_days).__dict__)
    list_exercises.append (workout_day (4, "arms", arms_4_days).__dict__)
    list_exercises.append (workout_day (4, "legs", legs_day).__dict__)
    list_exercises.append (workout_day (5, "cardio", cardio).__dict__)

    print(list_exercises)

    default_exercises_table.insert_many(list_exercises)

# create_default_exercises(default_exercises_table=None)

push_data_base_3_days = ["barbel_bench_press", "shoulders_presses","triceps", "chest_cable_crossover", "shoulders_dumble_lateral_raises", "triceps2"]

pull_data_base_3_days = ["pullups","bent_over_row","biceps","lat_pulldown","seated_row","biceps2"]

legs_day = ["squat", "romanina_deadlift", "bulgarian_split_squat", "calf_raise", "leg_extensions", "leg_curls"]

push_4_days = ["barbel_bench_press", "dips", "chest_cable_crossover", "dumbbell_bench_press", "chest_incline_fly", "machine_chest_press"]

pull_4_days = ["pullups", "bent_over_row", "single_arm_row", "lat_pulldown", "seated_row"]

arms_4_days =  ["shoulders_presses", "triceps1", "biceps1", "shoulders_dumble_lateral_raises", "triceps2", "biceps2"]

cardio = ["Threadmill", "Bicycle"]

def display_exercises (db, number_of_days, default_exercises_table):

    number_of_days = db.get_collection("Exercises")
    get_exercises = number_of_days.find_one({ "Exercises.number_of_days": 3, 
                                             "default_exercises_table" : default_exercises_table
                                            })

    if get_exercises == 3 :
        print ("Lista cu exercitiile")
