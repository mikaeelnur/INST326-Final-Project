from datetime import datetime, timedelta
import unittest

class Habit:
    def __init__(self, name, goal_frequency, current_streak=0, longest_streak=0, last_logged_date=None):
        """ Initialize name, goal_frequency, current_streak, longest_streak, and last_logged_date."""
        self.name = name
        self.goal_frequency= goal_frequency
        self.current_streak= current_streak
        self.longest_streak= longest_streak
        self.last_logged_date= last_logged_date

class HabitTracker:
    def __init__(self, file_path):
        """ Initializes the habit tracker object with an empty list of habits and loads file for data."""
        self.habit_list = []
        self.file_path = file_path
        self.load_from_file()

    def save_to_files(self):
        """ Saves all habits to the file"""
        with open(self.file_path, "w") as file:
            for habit in self.habit_list:
                last_logged = habit.last_logged_date.strftime("%m-%d-%Y") if habit.last_logged_date else ""
                line = f"{habit.name}, {habit.goal_frequency}, {habit.current_streak}, {habit.longest_streak}, {last_logged} \n"
                file.write(line)
    
    def load_from_file(self):
        """Load habits from the file."""
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    name = parts [0]
                    goal_frequency = int(parts [1])
                    current_streak = int(parts[2])
                    longest_streak = int(parts [3])
                    last_logged_date= datetime.strptime(parts[4], "%m-%d-%Y") if parts[4] else None
                    habit = Habit(name, goal_frequency, current_streak, longest_streak, last_logged_date)
                    self.habit_list.append(habit)
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")

    def add_habit (self, name, goal_frequency):
        """ Adds a new habit and saves it to the file.
        Parameters:  
        name (str): The name of the habit. 
        goal_frequency (int): The goal frequency for the habit, how often the habit should be completed. 
        Returns: None """

        new_habit = Habit(name, goal_frequency)
        self.habit_list.append(new_habit)
        self.save_to_file()
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
                self.save_to_file()
                print(f"Habit '{habit_name}' successfully removed.")
                return

    def log_progress (self, habit_name, date_logged):
        """Logs the progress of a habit by updating its streak based on the date logged
        Parameters:
        habit_name (str): The name of the habit. 
        date_logged (datetime): The date when progress is logged.
        habits (list): A list of habit dictionaries
        Returns: None """
        
        for habit in self.habit_list:
            if habit.name == habit_name:
                if not isinstance(date_logged, datetime):
                    raise TypeError("date_logged must be a datetime object.")

                if habit.last_logged_date is None:
                    habit.current_streak = 1
                else:
                    delta_days = (date_logged - habit.last_logged_date).days
                    

    def display_all_habits (habit_list):
        """Displays information for each habit in the habit list. 
        Parameters: 
        habit_list (list): A list of habit objects to display. 
        Returns: None """

        for habit in habit_list:
            print(f"Habit: {habit.name}")
            print(f"  Current Streak: {habit.current_streak}")
            print(f"  Longest Streak: {habit.longest_streak}")
            print()

    def show_overall_progress (habit_list):
        """Generates and returns a progress summary for each habit in the habit list.
        Parameters: 
        habit_list (list): A list of habits being tracked.
        Returns:
        str: A formatted string summarizing the name, current streak, and longest streak for each habit, 
        as well as an overall progress summary."""

        if not isinstance(habit_list, list):
            raise TypeError("habit_list must be a list of habit dictionaries.")
    if not all(isinstance(habit, dict) for habit in habit_list):
        raise ValueError("Each habit in habit_list must be a dictionary.")


    total_habits = len(habit_list)
    total_current_streak = 0
    habit_summaries = []


    for habit in habit_list:
        name = habit.get('name', 'Unnamed Habit')
        current_streak = habit.get('current_streak', 0)
        longest_streak = habit.get('longest_streak', 0)

        habit_summaries.append(f"{name}: Current Streak = {current_streak}, Longest Streak = {longest_streak}")
        total_current_streak += current_streak


    average_current_streak = total_current_streak / total_habits if total_habits > 0 else 0

 
    summary = "\n".join(habit_summaries)
    summary += f"\n\nTotal Habits: {total_habits}, Average Current Streak: {average_current_streak:.2f}"

    return summary

#Unit tests

class TestHabitTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = HabitTracker("test_habits.txt")
        self.tracker.habit_list = []
        self.tracker.add_habit("Go on a walk", 4)
        self.tracker.add_habit("Read before bed", 5)

    def test_add_habit(self):
        self.tracker.add_habit("Meditate", 7)
        self.assertEqual(len(self.tracker.habit_list), 3)
        self.assertEqual(self.tracker.habit_list[-1].name, "Meditate")

    def test_delete_habit(self):
        self.tracker.delete_habit("Read before bed")
        self.assertEqual(len(self.tracker.habit_list), 1)

    def test_log_progress(self):
        today - datetime.now()
        self.tracker.log_progress("Go on a walk", today)
        habit = next(h for h in self.tracker.habit_list if h.name=="Go on a walk")
        self.assertEqual(habit.current_streak, 1)

if __name__ == "__main__":
    #uncomment lines to run it
    # tracker = HabitTracker ("habits.txt")
    # habit_name = input ("Enter what habit you completed today: ")
    # tracker.log_progress(habit_name, datetime.now())
    # tracker.display_all_habits()

    #to run the unit tests
    unittest.main()


""" PLANNED UNIT TESTS:
Our unit tests will check each method to ensure that the code works properly. First, it will check if there 
is an existing txt file in the directory, if not, it will create a new txt file. After, we will input user 
data like specific habits, frequency, and test the streak counter. This will test if our code is successful
or not. From there, we will make corrections as needed.

"""