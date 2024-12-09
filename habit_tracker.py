from datetime import datetime, timedelta
import sqlite3

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
    def __init__(self, db_path="habits.db"):
        self.db_path = db_path
        self.habit_list = []
        self.initialize_database()
        self.load_from_database()

    def initialize_database(self):
        """Creates the habits table if it does not exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    goal_frequency INTEGER NOT NULL,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    last_logged_date TEXT
                )
            """)

    def load_from_database(self):
        """Loads habits from the database."""
        self.habit_list = []  # Clear current list
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, goal_frequency, current_streak, longest_streak, last_logged_date FROM habits")
            for row in cursor.fetchall():
                name, goal_frequency, current_streak, longest_streak, last_logged_date = row
                last_logged_date = datetime.strptime(last_logged_date, "%Y-%m-%d") if last_logged_date else None
                habit = Habit(name, goal_frequency, current_streak, longest_streak, last_logged_date)
                self.habit_list.append(habit)
    
    def save_to_database(self, habit):
        """Inserts or updates a habit in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO habits (name, goal_frequency, current_streak, longest_streak, last_logged_date)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    goal_frequency=excluded.goal_frequency,
                    current_streak=excluded.current_streak,
                    longest_streak=excluded.longest_streak,
                    last_logged_date=excluded.last_logged_date
            """, (habit.name, habit.goal_frequency, habit.current_streak, habit.longest_streak, 
                  habit.last_logged_date.strftime("%Y-%m-%d") if habit.last_logged_date else None))


    def _add_habit(self, name, goal_frequency):
        """Adds a new habit and saves it to the database."""
        new_habit = Habit(name, goal_frequency)
        self.habit_list.append(new_habit)
        self.save_to_database(new_habit)
        print(f"Habit '{name}' added successfully.")


    def delete_habit(self, habit_name):
        """Deletes a habit from the database and the habit list."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM habits WHERE name = ?", (habit_name,))
            if cursor.rowcount > 0:
                self.habit_list = [h for h in self.habit_list if h.name != habit_name]
                print(f"Habit '{habit_name}' successfully removed.")
            else:
                print(f"Habit '{habit_name}' not found.")


    def log_progress(self, habit_name, date_logged):
        """Logs progress for a habit and updates the database."""
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
                self.save_to_database(habit)
                print(f"Progress logged for habit '{habit_name}'. Current streak: {habit.current_streak}.")
                return

        print(f"Habit '{habit_name}' not found.")

    def display_all_habits (self):
        """Displays information for each habit in the habit list. 
        Parameters: 
        habit_list (list): A list of habit objects to display. 
        Returns: None
        """
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
        """Display a summary of overall progress across all habits.
        Calculates the total number of habits, the average current streak across all the habits, and
        individual summaries for each habit.
        Parameters:
        None
        Returns:
        None
        """
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