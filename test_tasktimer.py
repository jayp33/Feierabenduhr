import unittest
from datetime import time
from tasktimer import calculate_closing_time

class TestTaskTimer(unittest.TestCase):
    def test_calculate_closing_time(self):
        task_time = time(17, 0)  # 17:00
        task_timer_work_duration = 540  # 9 hours
        work_duration = 480  # 8 hours

        expected_closing_time = time(16, 0)  # 16:00
        result = calculate_closing_time(task_time, task_timer_work_duration, work_duration)
        self.assertEqual(result, expected_closing_time)

if __name__ == '__main__':
    unittest.main()