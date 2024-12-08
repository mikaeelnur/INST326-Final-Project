from habit_tracker import HabitTracker
from datetime import datetime
import unittest

#Unit tests
class TestHabitTracker(unittest.TestCase):
    """ Unit tests for the HabitTracker class"""
    
    def setUp(self):
        """    
        Sets up a new HabitTracker instance for testing purposes.
        
        Creates a new tracker using a temporary file, test_habits.txt.
        Initializes it with two default habits, "Go on a walk" and "Read before bed".
        """
        self.tracker = HabitTracker("test_habits.txt")
        self.tracker.habit_list = []
        self.tracker.add_habit("Go on a walk", 4)
        self.tracker.add_habit("Read before bed", 5)

    def test_add_habit(self):
        """ 
        Tests the add habit method

        This test ensures that when a new habit is added ("Meditate"), the number of
        habits in the tracker increases by 1. It also checks that the habit
        has the correct name and weekly goal.
        """
        self.tracker.add_habit("Meditate", 7)
        self.assertEqual(len(self.tracker.habit_list), 3)
        self.assertEqual(self.tracker.habit_list[-1].name, "Meditate")

    def test_delete_habit(self):
        """
        Tests the delete habit method.

        This test checks if "Read before bed" is deleted by ensuring the
        number of habits in the tracker is deleted by 1 and the habit no
        longer exists in the habit list.
        """
        self.tracker.delete_habit("Read before bed")
        self.assertEqual(len(self.tracker.habit_list), 1)
        habit_names = [habit.name for habit in self.tracker.habit_list]
        self.assertNotIn("Read before bed", habit_names)

    def test_log_progress(self):
        """
        Tests the log progress method.

        This test makes sure the streak for the habit is updated correctly.
        It also checks if the last logged date is set to the current date and 
        the longest streak is updated if the new streak exceeds the previous.
        """
        today = datetime.now()
        self.tracker.log_progress("Go on a walk", today)
        habit = next(h for h in self.tracker.habit_list if h.name=="Go on a walk")
        self.assertEqual(habit.current_streak, 1)
        self.assertEqual(habit.last_logged_date, today)
        self.assertEqual(habit.longest_streak, 1)
    
    def test_add_log_new_habit(self):
        """
        Tests adding and logging progress for a new habit

        This test verifies that if a habit doesn't exist it is added and the streak is
        set to 1. Also that the goal frequency is what the user set it as.
        """
        today= datetime.now()
        self.tracker.log_progress("Evening meditation", today)
        habit = next(h for h in self.tracker.habit_list if h.name == "Evening meditation")
        self.assertEqual(habit.current_streak, 1)
        self.assertEqual(habit.goal_frequency, 7)

    #run the unit tests
    unittest.main()