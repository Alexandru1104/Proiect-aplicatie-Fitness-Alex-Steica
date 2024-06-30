
import Baza_de_date.Sign_up_and_login as login_utils
# import Data_base_info
import User_info
import Custom_exercises_UI
import os

############# TO DELETE !!!! 

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
def get_db ():

    user_pass = "Mamatata92!"
    uri = f"mongodb+srv://alexsteica04:{user_pass}@alexsteica.izupp4r.mongodb.net/?retryWrites=true&w=majority&appName=AlexSteica"

    User = MongoClient(uri, server_api=ServerApi('1'))

    db = User.get_database("data_base_fitness_app")
    return db

#### PANA AICI !!! 

start_menu = {
    "Sign up " : [login_utils.sign_up, ["First name", "Last name", "Age", "email", "Username", "Password", "Password again"]],
    "Login " : [login_utils.login,["email", "password"]]
                }

logged_in_menu = {

    "Log workout" : [Custom_exercises_UI.log_workout, []],
    "Show progress" : [],
    "Reset account" : [],
    "Logout" : [login_utils.logout, []],
    "Delete account" : [login_utils.delete_account, []]

}

def display_menu(options_menu):

    counter = 1
    print("Press a key below to select an option : ")
    for option_menu in options_menu:
        print(f"{counter}. {option_menu}")
        counter += 1

def input_menu_cmd(options_menu: dict):
    while True:
        selected_option = int(input("Insert your desired key here : "))
        selected_option -= 1
        if selected_option < 0 or selected_option >= len(options_menu):
            print("Choose a valid option!")
            continue
        return selected_option

def show_menu (db):

    while True:
        os.system("cls")
        is_logged_in = User_info.get_current_usr().get_is_logged_in_variable()
        if not is_logged_in:
            menu = start_menu
        else :
            print (User_info.get_current_usr().get_is_set_up_variable ())
            if not User_info.get_current_usr().get_is_set_up_variable () :
                login_utils.set_up_account(db)
                User_info.get_current_usr().set_is_set_up_variable(True)
            menu = logged_in_menu

        display_menu (menu)
        index_cmd = input_menu_cmd(menu)

        options_list = list(menu.keys())
        selected_option = options_list[index_cmd]
        function, explain_arguments = menu[selected_option]

        arguments: list = [db]
        for explanation in explain_arguments:
            argument = input(f"Introduce argument for {explanation}: ")
            if argument.lower() == "stop":
                return
            arguments.append(argument)

        function(*arguments)
        input("Press any key to continue")

show_menu(get_db())







