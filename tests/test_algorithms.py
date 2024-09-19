# tests/test_algorithms.py

import unittest
from eduscheduler.algorithms.ilp_scheduler import generate_schedule_ilp
from eduscheduler.algorithms.genetic_scheduler import generate_schedule_genetic
from eduscheduler.database.db_manager import create_session

class TestSchedulingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.session = create_session()
        # Set up test data in the database

    def test_ilp_scheduler(self):
        schedule = generate_schedule_ilp(self.session)
        self.assertIsNotNone(schedule)
        # Additional assertions

    def test_genetic_scheduler(self):
        schedule = generate_schedule_genetic(self.session)
        self.assertIsNotNone(schedule)
        # Additional assertions

if __name__ == '__main__':
    unittest.main()
