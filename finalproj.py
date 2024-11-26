import datetime

class Habit:
    def __init__(self, name, goal_frequency):
        """ Initialize name, goal_frequency, current_streak, longest_streak, and last_logged_date."""
        self.name = name
        self.goal_frequency= goal_frequency
        self.current_streak= 0
        self.longest_streak= 0
        self.last_logged_date= None

class HabitTracker:
    def __init__(self):
        """ Initializes the habit tracker object with an empty list of habits."""
        self.habit_list = []

    def add_habit (self, name, goal_frequency):
        """ Creates a new habit object with the name and goal frequency, and adds it to the list.
        Parameters:  
        name (str): The name of the habit. 
        goal_frequency (int): The goal frequency for the habit, how often the habit should be completed. 
        Returns: None """

        new_habit = Habit(name, goal_frequency)
        self.habit_list.append(new_habit)
        print(f"Habit '{name}' added succesfully.")

    def delete_habit (self, habit_name):
        """ Finds a habit by name in the habit list and removes it.
        Parameters: 
        habit_list (list): The list of habits. 
        habit_name (str): The name of the habit to be removed. 
        Returns: None """
        for habit in self.habit_list:
            if habit.name== habit_name:
                self.habit_list.remove(habit)
                print(f"Habit '{habit_name}' successfully removed.")
                return

    def log_progress (habit_name, date_logged):
        """Logs the progress of a habit by updating its streak based on the date logged
        Parameters:
        habit_name (str): The name of the habit. 
        date_logged (): The date when progress is logged.
        Returns: None """

    def display_all_habits (habit_list):
        """Displays information for each habit in the habit list. 
        Parameters: 
        habit_list (list): A list of habit objects to display. 
        Returns: None """

    def show_overall_progress (habit_list):
        """Generates and returns a progress summary for each habit in the habit list.
        Parameters: 
        habit_list (list): A list of habits being tracked.
        Returns:
        str: A formatted string summarizing the name, current streak, and longest streak for each habit, 
        as well as an overall progress summary."""

""" PLANNED UNIT TESTS:
Our unit tests will check each method to ensure that the code works properly. First, it will check if there 
is an existing txt file in the directory, if not, it will create a new txt file. After, we will input user 
data like specific habits, frequency, and test the streak counter. This will test if our code is successful
or not. From there, we will make corrections as needed.

"""