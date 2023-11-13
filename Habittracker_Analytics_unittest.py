import unittest
from unittest.mock import patch, MagicMock # Mocking is to isolate the unit tests from the real database and its interactions(More from this link https://docs.python.org/3/library/unittest.mock.html)
from io import StringIO
from Habit_tracker_script import Analytics # retrieve Analytics class from the Habit_tracker_script.py module

class TestAnalytics(unittest.TestCase):

    # assertion method: takes the 3 parameters
    # compares the actual output in the mock_stdout to the expected output
    # The output is stripped before the comparison.
    def assert_stdout(self, expected_output, mock_stdout):
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch('sys.stdout', new_callable=StringIO) # patch here temporarily replace the sys.stdout (standard output) with a StringIO object during the execution of the this function
    def test_view_longest_streaks(self, mock_stdout):
        # (because of attribute error of "check streak" in prior tests) Mock the check_streak method in the Analytics class
        #The side_effect parameter specifies the return values when check_streak is called, where it returns 5 the first time and 3 the second time
        with patch('Habit_tracker_script.Analytics.check_streak', side_effect=[5, 3]): 
            analytics = Analytics()
            analytics.view_longest_streaks()
            expected_output = "Habit Name | Periodicity | Longest Streak (Days)\nExercise | daily | 5\nReading | weekly | 3"
            self.assert_stdout(expected_output, mock_stdout) #compare the captured output (mock_stdout.getvalue().strip()) with the expected output (test verifies that the method is producing the correct output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_daily_habits(self, mock_stdout):
        # Mock the execute method of the cursor in the view_daily_habits method
        with patch('Habit_tracker_script.cursor.execute') as mock_execute:
            mock_execute.return_value.fetchall.return_value = [
                (1, 'Exercise', 'Mon,Tue,Wed', '2023-01-01', '2023-01-02'),
                (2, 'Reading', 'Mon,Wed,Fri', '2023-01-01', '2023-01-03')
            ]
            analytics = Analytics()
            analytics.view_daily_habits()
            expected_output = "ID | Habit Name | Periodicity | Target Times/Days | Creation Date | Completed | Completion Date\n1 | Exercise | Daily | Mon,Tue,Wed | 2023-01-01 | Yes | 2023-01-02\n2 | Reading | Daily | Mon,Wed,Fri | 2023-01-01 | Yes | 2023-01-03"
            self.assert_stdout(expected_output, mock_stdout)

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_weekly_habits(self, mock_stdout):
        with patch('Habit_tracker_script.cursor.execute') as mock_execute:
            mock_execute.return_value.fetchall.return_value = [
                (1, 'Exercise', 'Mon,Wed,Fri', '2023-01-01', '2023-01-02'),
                (2, 'Reading', 'Mon,Tue,Wed', '2023-01-01', '2023-01-03')
            ]
            analytics = Analytics()
            analytics.view_weekly_habits()
            expected_output = "ID | Habit Name | Periodicity | Target Times/Days | Creation Date | Completed | Completion Date\n1 | Exercise | Weekly | Mon,Wed,Fri | 2023-01-01 | Yes | 2023-01-02\n2 | Reading | Weekly | Mon,Tue,Wed | 2023-01-01 | Yes | 2023-01-03"
            self.assert_stdout(expected_output, mock_stdout)

if __name__ == '__main__':
    unittest.main()





