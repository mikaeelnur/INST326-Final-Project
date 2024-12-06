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

# This tracks a collection of habits and provides operations to manage and analyze them.
class HabitTracker:
    def __init__(self, file_path):
        """ Initializes the habit tracker object with an empty list of habits and loads file for data."""
        self.habit_list = [] # List to store Habit objects
        self.file_path = file_path # File path for saving and loading habits
        self.load_from_file() # Load existing habits from the file

    def save_to_file(self):
        """ Saves all habits to the file"""
        with open(self.file_path, "w") as file:
            for habit in self.habit_list:
                # Format the last_logged_date if it exists, otherwise leave it blank
                last_logged = habit.last_logged_date.strftime("%m-%d-%Y") if habit.last_logged_date else ""
                # Write habit details to a txt file.
                line = f"{habit.name}, {habit.goal_frequency}, {habit.current_streak}, {habit.longest_streak}, {last_logged}\n"
                file.write(line)
    
    def load_from_file(self):
        """Load habits from the file."""
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    # Split each line to extract habit attributes
                    parts = line.strip().split(",")
                    name = parts[0].strip()
                    goal_frequency = int(parts [1].strip())
                    current_streak = int(parts[2].strip())
                    longest_streak = int(parts [3].strip())
                    # Parse the last_logged_date if it exists
                    last_logged_date= datetime.strptime(parts[4].strip(), "%m-%d-%Y") if parts[4].strip() else None
                    # Create a Habit object and add it to the list
                    habit = Habit(name, goal_frequency, current_streak, longest_streak, last_logged_date)
                    self.habit_list.append(habit)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist
            print(f"File '{self.file_path}' not found. Creating a new one.")

    def add_habit (self, name, goal_frequency):
        """ Adds a new habit and saves it to the file.
        Parameters:  
        name (str): The name of the habit. 
        goal_frequency (int): The goal frequency for the habit, how often the habit should be completed. 
        Returns: None """

        new_habit = Habit(name, goal_frequency) # Create a new Habit object
        self.habit_list.append(new_habit) # Add it to the habit list
        self.save_to_file() # Save the updated list to the file
        print(f"Habit '{name}' added succesfully.")

    def delete_habit (self, habit_name):
        """ Finds a habit by name in the habit list and removes it.
        Parameters: 
        habit_list (list): The list of habits. 
        habit_name (str): The name of the habit to be removed. 
        Returns: None """
        if not self.habit_list:
            print("No habits to delete, list is empty.")
        for habit in self.habit_list:
            if habit.name== habit_name: # Find the habit by name
                self.habit_list.remove(habit) # Remove it from the list
                self.save_to_file() # Save the updated list to the file
                print(f"Habit '{habit_name}' successfully removed.")
                return
        print(f"Habit '{habit_name}' not found. No habits were deleted.")

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
                    if delta_days == 1:
                        habit.current_streak += 1
                    elif delta_days > 1:
                        habit.current_streak = 1
                    else:
                        raise ValueError("date_logged cannot be earlier than the last logged date.")
                
                habit.longest_streak = max(habit.longest_streak, habit.current_streak)
                habit.last_logged_date = date_logged
                self.save_to_file()
                print(f"Progress logged for habit '{habit_name}'. Current streak: {habit.current_streak}.")
                return
        
        print(f"Habit '{habit_name}' not found.")
        goal_frequency= int(input("Enter the goal frequency for this habit (# of times per week): "))
        self.add_habit(habit_name, goal_frequency)


    def display_all_habits (self):
        """Displays information for each habit in the habit list. 
        Parameters: 
        habit_list (list): A list of habit objects to display. 
        Returns: None"""
        
        if not self.habit_list: # Check if the list is empty
            print("No habits to display.")
        else:
            for habit in self.habit_list:
                # Print details of each habit
                print(f"Habit: {habit.name}")
                print(f"  Goal Frequency: {habit.goal_frequency} times/week")
                print(f"  Current Streak: {habit.current_streak}")
                print(f"  Longest Streak: {habit.longest_streak}")
                print(f"  Last Logged: {habit.last_logged_date}")
                print()

    def show_overall_progress(self):
            """Display a summary of overall progress across all habits."""
            if not self.habit_list:
                print("No habits to summarize.")
                return
                
            # Calculate total habits and streak averages
            total_habits = len(self.habit_list)
            total_streaks = sum(habit.current_streak for habit in self.habit_list)
            habit_summaries = [
                f"{habit.name}: Current Streak = {habit.current_streak}, Longest Streak = {habit.longest_streak}"
                for habit in self.habit_list
            ]

            average_streak = total_streaks / total_habits if total_habits > 0 else 0
        # Display a summary for each habit
            print("\nOverall Progress Summary:")
            print("\n".join(habit_summaries))
            print(f"\nTotal Habits: {total_habits}")
            print(f"Average Current Streak: {average_streak:.2f}")


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
        habit_names = [habit.name for habit in self.tracker.habit_list]
        self.assertNotIn("Read before bed", habit_names)

    def test_log_progress(self):
        today = datetime.now()
        self.tracker.log_progress("Go on a walk", today)
        habit = next(h for h in self.tracker.habit_list if h.name=="Go on a walk")
        self.assertEqual(habit.current_streak, 1)
        self.assertEqual(habit.last_logged_date, today)
        self.assertEqual(habit.longest_streak, 1)
    
    def test_add_log_new_habit(self):
        today= datetime.now()
        self.tracker.log_progress("Evening meditation", today)
        habit = next(h for h in self.tracker.habit_list if h.name == "Evening meditation")
        self.assertEqual(habit.current_streak, 1)
        self.assertEqual(habit.goal_frequency, 7)

if __name__ == "__main__":
    tracker = HabitTracker ("habits.txt")
    while True:
        print("\nHabit Tracker Menu:" )
        print("1. Add a new habit")
        print("2. Log progress for a habit")
        print("3. Display all habits")
        print("4. Show overall progress")
        print("5. Delete a habit")
        print("6. Exit")

        choice = input("Enter your choice (#): ")

        if choice == "1":
            habit_name = input("Enter the name of the habit: ")
            try:
                goal_frequency = int(input("Enter the goal frequency for this habit (times per week): "))
                tracker.add_habit(habit_name, goal_frequency)
            except ValueError:
                print("Invalid input. Goal frequency must be a number.")
        elif choice == "2":
            habit_name = input("Enter the name of the habitat you completed today: ")
            tracker.log_progress(habit_name, datetime.now())
        elif choice == "3":
            tracker.display_all_habits()
        elif choice == "4":
            tracker.show_overall_progress()
        elif choice == "5":
            habit_name = input("Enter the habit to delete:" )
            tracker.delete_habit(habit_name)
        elif choice == "6":
            print ("Exiting habit tracker.")
            break
        else:
            print("Invalid choice. Please try again with a valid option.")

    #uncomment to run the unit tests
    #unittest.main()
