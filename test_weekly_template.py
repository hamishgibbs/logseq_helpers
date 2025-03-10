import unittest
from datetime import datetime
from weekly_template import compute_monday

class TestComputeMonday(unittest.TestCase):
    def test_monday_input(self):
        # When the date is already Monday, it should return the same date
        date = datetime(2023, 10, 9)  # Monday
        self.assertEqual(compute_monday(date), date)

    def test_tuesday(self):
        # Tuesday should return the previous Monday
        date = datetime(2023, 10, 10)  # Tuesday
        expected = datetime(2023, 10, 9)
        self.assertEqual(compute_monday(date), expected)

    def test_sunday(self):
        # Sunday should return the Monday of that week
        date = datetime(2023, 10, 15)  # Sunday
        expected = datetime(2023, 10, 9)
        self.assertEqual(compute_monday(date), expected)

if __name__ == '__main__':
    unittest.main()
