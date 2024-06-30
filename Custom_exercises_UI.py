
import tkinter as tk
from tkinter import ttk
import Data_base.Exercises as exercises
import User_info
import Data_base.Data_base_info as Data_base_info


list_days = []
list_exercises = []

def add_in_db (custom_exercises_tk):

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
    print(selected_exercises_dict)



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

    button_fetch = tk.Button(custom_exercises_tk, text="Submit", command = lambda : add_in_db(custom_exercises_tk))
    button_fetch.grid (row = 4, column = total_days // 2, padx = 10, pady = 20)
    custom_exercises_tk.mainloop()



def log_workout (db):
     
    log_workout_tk = tk.Tk()
    log_workout_tk.title("Log your exercises")
    log_workout_tk.geometry("1000x550")

    list_of_splits = []
    selected_exercises = db.get_collection("Selected exercises")
    user_exercises = selected_exercises.find_one({ "email": User_info.get_current_usr().get_email_variable()}) 
    if user_exercises ["workout"] == "default" :
         default_exercises = db.get_collection("Default exercises")
         list_of_default_entries = default_exercises.find({"number_of_days" : User_info.get_current_usr().get_gym_days_variable()})
         for default_entries in list_of_default_entries :
            list_of_splits.append(default_entries ["type_of_exercise"])
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

def log_exercises_in_db (db, log_workout_tk) :
    logged_exercises = db.get_collection("Logged exercises")
    entry = logged_exercises.find_one({"email" : User_info.get_current_usr().get_email_variable()})
    
    if not entry :
        insert_user = {
            "email" : User_info.get_current_usr().get_email_variable(),
            "history" : []
        }
        logged_exercises.insert_one(insert_user)

    else : 

        logged_exercises.find_one({"email" : User_info.get_current_usr().get_email_variable()})

    

def display_data (db, log_workout_tk, selected_day) :

    selected_exercises = db.get_collection("Selected exercises")
    user_exercises = selected_exercises.find_one({ "email": User_info.get_current_usr().get_email_variable()}) 

    if user_exercises ["workout"] == "default" :
        default_exercises = db.get_collection("Default exercises")
        workout_day_exercises = default_exercises.find_one({"number_of_days" : User_info.get_current_usr().get_gym_days_variable(), "type_of_exercise" : selected_day})
        list_of_exercises = workout_day_exercises["list_of_exercise"]
    else : 
        for workout_day in user_exercises ["workout"] :
            if int (workout_day ["number_of_days"]) == int (User_info.get_current_usr().get_gym_days_variable())  and workout_day ["type_of_exercise"] == selected_day : 
                list_of_exercises = workout_day["list_of_exercise"]
                print(workout_day)
    
    
    ct = 0

    for exercise in list_of_exercises :
        label_id = tk.Label(log_workout_tk, text = exercise)
        label_id.grid (row = 3 + ct, column = 0, padx = 10, pady = 20)

        series_no = tk.Entry(log_workout_tk, width=20)
        series_no.grid (row = 3 + ct, column = 1, padx = 10, pady = 20)

        repetitions = tk.Entry(log_workout_tk, width=20)
        repetitions.grid (row = 3 + ct, column = 2, padx = 10, pady = 20)

        weight = tk.Entry(log_workout_tk, width=20)
        weight.grid (row = 3 + ct, column = 3, padx = 10, pady = 20)

        ct += 1

    button_fetch = tk.Button(log_workout_tk, text="Submit", command = lambda : log_exercises_in_db(db, log_workout_tk))
    button_fetch.grid (row = 3 + ct, column = 1, padx = 10, pady = 20)


