
from re import L
import Custom_exercises_UI as Exercises_UI
import User_info

########################################################################
# Description: Function used to create new user
# Queries DB: 
#   - find_one -> to check if user already exists in db (Users collection)
#   - insert_one -> to insert the new user in db (Users collection)
# Parameters:
#    - db : database -> object for database
#    - user_input_first_name: string
#    - user_input_last_name: string 
#    - user_input_age: integer 
#    - user_input_email: string 
#    - user_input_username: string 
#    - user_input_password: string
#    - user_input_password_check: string -> used to double check the psswd
# Returns: no return
########################################################################
def sign_up (db, user_input_first_name, user_input_last_name, user_input_age, user_input_email, user_input_username, user_input_password, user_input_password_check) :

    username_table = db.get_collection("Users")

    # Check if email exists. If yes, another email is required
    email_exists = username_table.find_one({ "User.email": user_input_email})

    while email_exists :
        user_input_email = input("email already exists, please introduce another one : ")
        email_exists = username_table.find_one({ "User.email": user_input_email})

    # Check if username exists. If yes, another username is required
    username_exists = username_table.find_one({ "User.username": user_input_username})

    while username_exists :
        user_input_username = input("Username already exists, please introduce another one : ")
        username_exists = username_table.find_one({ "User.username": user_input_username})

    while user_input_password != user_input_password_check :
        user_input_password_check = input("Introduced password is not the same, please introduce second password again : ")

    username_table.insert_one({"User":{"First name": user_input_first_name, 
                            "Last name" : user_input_last_name,
                            "Age" : user_input_age,
                            "email" : user_input_email ,
                            "username" : user_input_username,
                            "password" : user_input_password,
                            "isSetUp" : False
                    }})

    print ("User sign up succesfully !! ")

########################################################################
# Description: Function used to login existing user
# Queries DB: 
#   - find_one -> to check if user exists in db and passwd matches
# Parameters:
#    - db : database -> object for database
#    - email: string -> email provided by user
#    - password: string -> password provided by user
# Actions:
#    - set up usr object defined in User_info.py with info from db
# Returns: no return
#######################################################################
def login (db, email, password) :
    
    username_table = db.get_collection("Users")
    user_exists = username_table.find_one({ "User.email": email, 
                                             "User.password" : password
                                            })

    if not user_exists :
        print ("Wrong user or password !! ")
        return
    print ("Login successful !! ")

    User_info.get_current_usr().set_email_variable(email)

    User_info.get_current_usr().set_is_logged_in_variable(True)

    selected_user = username_table.find_one({ "User.email": email}, {"User" : 1})

    User_info.get_current_usr().set_is_set_up_variable (selected_user["User"]["isSetUp"])

    if User_info.get_current_usr().get_is_set_up_variable() : 
        selected_exercises = db.get_collection("Selected exercises")
        selected_exercise = selected_exercises.find_one({"email" : User_info.get_current_usr().get_email_variable()})
        gym_days = selected_exercise["gym_days"]
        User_info.get_current_usr().set_gym_days_variable(gym_days)


########################################################################
# Description: Function that sets the isSetUp field on True for the current usr
#            : The function is called at the end of set_up_account()
# Queries DB: 
#   - update_one -> update the isSetUp field of the usr from False to True
# Parameters:
#    - db : database -> object for database
# Returns: no return
#######################################################################
def add_set_up_var_to_db(db) :

    username_table = db.get_collection("Users")
    filter_query = {"User.email": User_info.get_current_usr().get_email_variable()}
    new_values = {"$set":{"User.isSetUp" : True}}
    username_table.update_one(filter_query, new_values)

########################################################################
# Description: Function used on first login to setup user account
#            : User can select the number of gym days and the workout
#            : Gym days can be 3/4/5 and usr can use default or custom workout
# Queries DB: no query
# Parameters:
#    - db : database -> object for database
# Returns: no return
#######################################################################
def set_up_account (db) :  
    
    gym_days =int(input("How many days per week do you want to go to the gym (3/4/5) : "))
    while gym_days < 3 or gym_days > 5 :
       gym_days = int (input("Please choose between 3 and 5 days"))
    User_info.get_current_usr().set_gym_days_variable (gym_days)
    default_plan = input("Would you like to choose the default plan (y/n) : ")
    while default_plan not in ["y", "yes", "n", "no"] :
        default_plan = input("Please introduce your answer again (y/n) : ")
    if default_plan in ["y", "yes"] :
        print("Your default plan will is : ")
        display_default_plan(db, gym_days)
    else :
        display_custom_plan()

    add_set_up_var_to_db(db)

########################################################################
# Description: Function used if usr selects a custom plan creation
#            : It calls the set_custom_plan() function from Exercises UI module
# Queries DB: no query
# Parameters: no param
# Returns: no return
#######################################################################
def display_custom_plan ():

    Exercises_UI.set_custom_plan()

########################################################################
# Description: Function used if usr selects the default plan usage
#            : Display selected plan based on usr selection of gym days
# Queries DB: 
#    - find: find all entry in Default exercises collection that match the gym days number
#    - insert_one: insert entry in Selected exercises collection containing the
#                : current usr, number of gym days + exercises plan
# Parameters:
#    - db : database -> object for database
#    - number_of_days: integer -> number of gym days selected by usr
# Returns: no return
#######################################################################
def display_default_plan (db, number_of_days):

    default_exercises = db.get_collection("Default exercises")

    if number_of_days == 3:
        workout_days = default_exercises.find({ "number_of_days": 3 })
        print(f"You selected {number_of_days} workout days. Here is my suggestion for you:")
        for workout_day in workout_days :
            ct = 1
            print(workout_day["type_of_exercise"])
            print("-----------------------------------\n")
            for exercise in workout_day ["list_of_exercise"]:
                print(f"{ct}. {exercise}")
                ct+=1
            print("\n")
            
    elif number_of_days == 4 :

        workout_days = default_exercises.find({ "number_of_days": 4 })
        print(f"You selected {number_of_days} workout days. Here is my suggestion for you:")
        for workout_day in workout_days :
            ct = 1
            print(workout_day["type_of_exercise"])
            print("-----------------------------------\n")
            for exercise in workout_day ["list_of_exercise"]:
                print(f"{ct}. {exercise}")
                ct+=1
            print("\n")

    elif number_of_days == 5 :

        workout_days = default_exercises.find({ "number_of_days": 4 })
        print(f"You selected {number_of_days} workout days. Here is my suggestion for you:")
        for workout_day in workout_days :
            ct = 1
            print(workout_day["type_of_exercise"])
            print("-----------------------------------\n")
            for exercise in workout_day ["list_of_exercise"]:
                print(f"{ct}. {exercise}")
                ct+=1
            print("\n")
        workout_days = default_exercises.find({ "number_of_days": 5 })
        for workout_day in workout_days :
            ct = 1
            print(workout_day["type_of_exercise"])
            print("-----------------------------------\n")
            for exercise in workout_day ["list_of_exercise"]:
                print(f"{ct}. {exercise}")
                ct+=1
            print("\n")
    
    selected_exercises_dict = {}
    custom_exercises = db.get_collection("Selected exercises")
    selected_exercises_dict["email"] = User_info.get_current_usr().get_email_variable()
    selected_exercises_dict["workout"] = "default"
    selected_exercises_dict ["gym_days"] = User_info.get_current_usr().get_gym_days_variable()
    custom_exercises.insert_one (selected_exercises_dict)

########################################################################
# Description: Function used if usr wants to remove his account
# Queries DB: 
#    - delete_one: remove user from Users, Selected/Logged exercises tables
# Parameters:
#    - db : database -> object for database
#    - number_of_days: integer -> number of gym days selected by usr
# Returns: no return
#######################################################################
def delete_account (db) :
    
    are_you_sure = input ("Are you sure you want to delete your account? (y/n)")

    while are_you_sure not in ["y", "yes", "n", "no"] :
        are_you_sure = input("Please introduce your answer again (y/n) : ")
    if are_you_sure in ["y", "yes"] :
        print("Your user will be completly removed ")

        users_table = db.get_collection("Users")
        filter_query = {"User.email": User_info.get_current_usr().get_email_variable()}
        users_table.delete_one(filter_query)

        exercises_table = db.get_collection("Selected exercises")
        filter_query = {"email": User_info.get_current_usr().get_email_variable()}
        exercises_table.delete_one(filter_query)

        # TODO: check if this is still working
        logged_exercises_table = db.get_collection("Logged exercises")
        filter_query = {"email": User_info.get_current_usr().get_email_variable()}
        logged_exercises_table.delete_one(filter_query)

        User_info.get_current_usr().reset_user()
    
    else : 
        print("Congratulations you are still a member !! ")


########################################################################
# Description: Function used if usr wants to remove his account log out
#            : Resets all current user (object) information
# Queries DB: no queries
# Parameters:
#    - db : database -> object for database
# Returns: no return
####################################################################
def logout (db): 

    User_info.get_current_usr().reset_user()

    print("You have been logged out successfully" )


