
import tkinter as tk
from tkinter import ttk
import Data_base.Exercises as exercises
import User_info
import Data_base.Data_base_info as Data_base_info
import Log_workout_info
from datetime import datetime


list_days = []
list_exercises = []

########################################################################
# Description: Function used to take data from UI and insert it into db
#            : Function uses the controller IDs of the text boxes from the UI
#            : extracts the text inside, creates a dictionary and writes it in db
# Queries DB:
#   - insert_one: insert object containing email, gym_days and workout list
# Parameters:
#    - custom_exercises_tk : tkinter -> object for UI controller
# Returns: no return
####################################################################
def add_custom_plan_in_db (custom_exercises_tk):

    table_selected_exercises = Data_base_info.get_db().get_collection("Selected exercises")

    get_list_days = []
    get_list_exercises = []
    workout_days_list = []

    for element in list_days :
        get_list_days.append(element.get())

    for element in list_exercises :
        content = element.get("1.0", tk.END).strip()
        get_list_exercises.append (content.split("\n"))

    for day in range (len(get_list_exercises)) :
            workout_days_list.append (exercises.workout_day (User_info.get_current_usr().get_gym_days_variable(), get_list_days [day], get_list_exercises [day]).__dict__)

    selected_exercises_dict = {}

    selected_exercises_dict["email"] = User_info.get_current_usr().get_email_variable()
    selected_exercises_dict["workout"] = workout_days_list
    selected_exercises_dict["gym_days"] = User_info.get_current_usr().get_gym_days_variable()
    table_selected_exercises.insert_one (selected_exercises_dict)
    custom_exercises_tk.destroy()


########################################################################
# Description: Function used to create UI using tkinter module
#            : Creates labels and textboxes for user input
#            : Saves textboxes controller IDs in lists so that they can be read later
# Queries DB: no query
# Parameters: no params
# Returns: no return
####################################################################
def set_custom_plan () :

    custom_exercises_tk = tk.Tk()
    custom_exercises_tk.title("Add your exercises")
    custom_exercises_tk.geometry("1000x550")

    total_days = User_info.get_current_usr().get_gym_days_variable()

    for day in range (1, total_days + 1) :
    
        label_id = tk.Label(custom_exercises_tk, text=f"Insert your split for day {day}:")
        label_id.grid (row = 0, column = day, padx = 10, pady = 20)
        split_day = tk.Entry(custom_exercises_tk, width=20)
        split_day.grid (row = 1, column = day, padx = 10, pady = 20)
        list_days.append(split_day)

        label_id = tk.Label(custom_exercises_tk, text = "Insert your exercises :")
        label_id.grid (row = 2, column = day, padx = 10, pady = 20)
        exercise_list = tk.Text(custom_exercises_tk, wrap='word', height=10, width=20)
        exercise_list.grid (row = 3, column = day, padx = 10, pady = 20)
        list_exercises.append(exercise_list)

    button_fetch = tk.Button(custom_exercises_tk, text="Submit", command = lambda : add_custom_plan_in_db(custom_exercises_tk))
    button_fetch.grid (row = 4, column = total_days // 2, padx = 10, pady = 20)
    custom_exercises_tk.mainloop()

########################################################################
# Description: Function used to take data from UI needed for logging
#            : asks user to select a split day from a list
# Queries DB:
#   - find_one: find the split of the current user
# Parameters:
#    - db : database -> object for database
# Returns: no return
####################################################################
def log_workout (db):
     
    log_workout_tk = tk.Tk()
    log_workout_tk.title("Log your exercises")
    log_workout_tk.geometry("1000x550")

    list_of_splits = []
    selected_exercises = db.get_collection("Selected exercises")
    user_exercises = selected_exercises.find_one({ "email": User_info.get_current_usr().get_email_variable()})
    # if user chose the default workout, then we extract the list of split (push/pull/legs) from Default exercises table, based on the number of gym_days
    if user_exercises ["workout"] == "default" :
         default_exercises = db.get_collection("Default exercises")
         list_of_default_entries = default_exercises.find({"number_of_days" : User_info.get_current_usr().get_gym_days_variable()})
         for default_entries in list_of_default_entries :
            list_of_splits.append(default_entries ["type_of_exercise"])
    # if user chose the custom workout, then we extract the list of split (push/pull/legs) from Selected exercises table, based on the number of gym_days
    else : 
        list_of_entries = user_exercises["workout"]
        for entry in list_of_entries :
            list_of_splits.append(entry ["type_of_exercise"])

    label_id = tk.Label(log_workout_tk, text=f"Select your workout :")
    label_id.grid (row = 0, column = 0, padx = 10, pady = 20)

    selected_day = ""

    def on_select (event) :
        selected_day = combo.get ()
        display_data(db, log_workout_tk, selected_day)
    # the split days list is displayed on the dropdown; the user should select the split that they want to log
    # on select event, the graphical interface is displayed to the user, with the list of exercises to log
    combo = ttk.Combobox(log_workout_tk, values = list_of_splits)
    combo.grid(row = 1, column = 0, padx = 10, pady = 20)
    combo.bind("<<ComboboxSelected>>", on_select)
    combo.current(0)


    label_id = tk.Label(log_workout_tk, text = "Exercises name")
    label_id.grid (row = 2, column = 0, padx = 10, pady = 20)

    label_id = tk.Label(log_workout_tk, text = "Series no.")
    label_id.grid (row = 2, column = 1, padx = 10, pady = 20)

    label_id = tk.Label(log_workout_tk, text = "Repetitions")
    label_id.grid (row = 2, column = 2, padx = 10, pady = 20)

    label_id = tk.Label(log_workout_tk, text = "Weight (kg)")
    label_id.grid (row = 2, column = 3, padx = 10, pady = 20)


########################################################################
# Description: Called on user selection on the dropdown (combobox)
#            : for the current split, the UI will contain the list 
#            : of the selected day exercises
#            : Based on the list of controllers IDs, we extract user input
#            : On button click, call log_exercises_in_db()
# Queries DB:
#   - find_one: find the exercises list of the current user
# Parameters:
#    - db : database -> object for database
#    - log_workout_tk: tk -> object for user UI
#    - selected_day: string -> selected by user from dropdown (push/pull..etc)
# Returns: no return
####################################################################
def display_data (db, log_workout_tk, selected_day) :

    # get from db collection with Selected exercises
    # extract from collection the entry for the current user
    selected_exercises = db.get_collection("Selected exercises")
    user_exercises = selected_exercises.find_one({ "email": User_info.get_current_usr().get_email_variable()}) 

    # if current user uses default workout, extract the list of exercises from default exercises table
    # else, extract list from the custom list saved in the Selected exercises table
    if user_exercises ["workout"] == "default" :
        default_exercises = db.get_collection("Default exercises")
        workout_day_exercises = default_exercises.find_one({"number_of_days" : User_info.get_current_usr().get_gym_days_variable(), "type_of_exercise" : selected_day})
        list_of_exercises = workout_day_exercises["list_of_exercise"]
    else : 
        for workout_day in user_exercises ["workout"] :
            if int (workout_day ["number_of_days"]) == int (User_info.get_current_usr().get_gym_days_variable())  and workout_day ["type_of_exercise"] == selected_day : 
                list_of_exercises = workout_day["list_of_exercise"]
                print(workout_day)

    row_ct = 0
    exercises_controllers_list = []
    series_no_controllers_list = []
    repetitions_controllers_list = []
    weight_controllers_list = []
    logger_controllers_dict = {}
    

    # for each exercises in the list (eg: bench press), create a label for the name and 3 text boxes (sets, repetitions and weight)
    # save the controllers of each label/textbox in lists so that we can get the text from them later in the code
    for exercise in list_of_exercises :
        exercise_lbl = tk.Label(log_workout_tk, text = exercise)
        exercise_lbl.grid (row = 3 + row_ct, column = 0, padx = 10, pady = 20)
        exercises_controllers_list.append(exercise_lbl)

        series_no_txt = tk.Entry(log_workout_tk, width=20)
        series_no_txt.grid (row = 3 + row_ct, column = 1, padx = 10, pady = 20)
        series_no_controllers_list.append(series_no_txt)

        repetitions_txt = tk.Entry(log_workout_tk, width=20)
        repetitions_txt.grid (row = 3 + row_ct, column = 2, padx = 10, pady = 20)
        repetitions_controllers_list.append(repetitions_txt)

        weight_txt = tk.Entry(log_workout_tk, width=20)
        weight_txt.grid (row = 3 + row_ct, column = 3, padx = 10, pady = 20)
        weight_controllers_list.append(weight_txt)

        row_ct += 1

    logger_controllers_dict["exercises_controllers_list"] = exercises_controllers_list.copy()
    logger_controllers_dict["series_no_controllers_list"] = series_no_controllers_list.copy()
    logger_controllers_dict["repetitions_controllers_list"] = repetitions_controllers_list.copy()
    logger_controllers_dict["weight_controllers_list"] = weight_controllers_list.copy()
    
    # submit button; on click, the log_exercises_in_db() function is called
    button_submit = tk.Button(log_workout_tk, text="Submit", command = lambda : log_exercises_in_db(db, log_workout_tk, logger_controllers_dict))
    button_submit.grid (row = 3 + row_ct, column = 1, padx = 10, pady = 20)


########################################################################
# Description: Called on button click from user UI window
#            : Takes data from user UI textboxes -> creates log_exercise objects
#            : Objects are written into db
# Queries DB:
#   - find_one: get the entry of the current usr in the Logged exercises table
#   - insert_one: insert new object for current usr if it is the FIRST time they log
#   - update_one: update existing entry for current usr if they already have logged before
# Parameters:
#    - db : database -> object for database
#    - log_workout_tk: tk -> object for user UI
#    - logger_controllers_dict: dict -> dictionary containing all controllers ID from the UI
#                                    -> controller IDs are used to extract text written by usr
# Returns: no return
####################################################################
def log_exercises_in_db (db, log_workout_tk, logger_controllers_dict) :
    logged_exercises_list = []
    logged_object_dictionary = {}

    number_of_exercises = len(logger_controllers_dict["exercises_controllers_list"])
    for i in range(number_of_exercises):
        # create object of type log_exercise by using the data provided by user in labels/textboxes
        log_ex = Log_workout_info.log_exercise(
            logger_controllers_dict["exercises_controllers_list"][i].cget("text"),
            logger_controllers_dict["series_no_controllers_list"][i].get(),
            logger_controllers_dict["repetitions_controllers_list"][i].get(),
            logger_controllers_dict["weight_controllers_list"][i].get()
        )
        # convert object of type log_exercise into dict and add it to list
        logged_exercises_list.append(log_ex.__dict__)

    # save current data in dictionary
    logged_object_dictionary["date"] = datetime.now().strftime("%d-%m-%Y")
    logged_object_dictionary["list_of_logged_exercises"] = logged_exercises_list

    # write previous dictionary to db
    logged_exercises = db.get_collection("Logged exercises")
    entry = logged_exercises.find_one({"email" : User_info.get_current_usr().get_email_variable()})

    # if first time when logging, create new entry in db for this user
    if entry is None :
        insert_user = {
            "email" : User_info.get_current_usr().get_email_variable(),
            "history" : [logged_object_dictionary]
        }
        logged_exercises.insert_one(insert_user)
    # if not first time when logging, update existing entry
    else : 
        logged_exercises_table = logged_exercises.find_one({"email" : User_info.get_current_usr().get_email_variable()})
        list_of_logged_exercises = logged_exercises_table["history"]
        list_of_logged_exercises.append(logged_object_dictionary)
        update = { "$set": { "history": list_of_logged_exercises } }
        logged_exercises.update_one({"email" : User_info.get_current_usr().get_email_variable()}, update)


