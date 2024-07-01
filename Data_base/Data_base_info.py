
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

########################################################################
# Description: Function to connect to dataBase
# Parameters: no params
# Returns:
#   - db : object containing database
########################################################################
def get_db ():

    user_pass = "Mamatata92!"
    uri = f"mongodb+srv://alexsteica04:{user_pass}@alexsteica.izupp4r.mongodb.net/?retryWrites=true&w=majority&appName=AlexSteica"

    User = MongoClient(uri, server_api=ServerApi('1'))

    db = User.get_database("data_base_fitness_app")
    return db







