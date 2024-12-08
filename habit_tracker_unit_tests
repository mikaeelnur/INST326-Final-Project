from habit_tracker import HabitTracker
from datetime import datetime
import unittest

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

    #run the unit tests
    unittest.main()