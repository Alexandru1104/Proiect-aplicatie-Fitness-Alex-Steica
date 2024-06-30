
class User :

    def __init__ (self) -> None:
        self.gym_days = 0
        self.is_logged_in = False
        self.is_set_up = False

    
    def set_email_variable (self, email) :
        self.email = email

    def get_email_variable (self): 
        return self.email

    def set_user_data (self, first_name, last_name, age, username, password) :
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.username = username
        self.password = password

    def set_is_logged_in_variable(self, value):
        self.is_logged_in = value

    def get_is_logged_in_variable(self):
        return self.is_logged_in

    def set_is_set_up_variable(self, value):
        self.is_set_up = value

    def get_is_set_up_variable(self):
        return self.is_set_up

    def set_gym_days_variable (self, value):
        self.gym_days = value

    def get_gym_days_variable(self):
        return self.gym_days
    
    def reset_user (self):
        self.gym_days = 0
        self.is_logged_in = False
        self.is_set_up = False

############# Global variables declaration section #############

usr = User()

def get_current_usr ():
    global usr
    return usr

################################################################



