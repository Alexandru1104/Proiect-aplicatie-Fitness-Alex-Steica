
# class used to create log_exercise object for creating a list of logged data from usr
class log_exercise :

    def __init__(self, name, series,repetitions, weight) -> None:
        
        self.name = name
        self.series = series
        self.repetitions = repetitions
        self.weight = weight

# class used to create log_entry object for putting together a list of logged data from usr
class log_entry :

    def __init__(self, date, list_of_logged_exercises) -> None:
        self.list_of_logged_exercises = list_of_logged_exercises
        self.date = date
