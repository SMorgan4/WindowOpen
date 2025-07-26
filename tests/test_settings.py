import unittest
from datetime import timedelta
from program_settings import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        pass

    def test_string_to_timedelta(self):
        self.assertEqual(Settings._string_to_timedelta("10:30"),timedelta(hours=10, minutes=30))
        self.assertEqual(Settings._string_to_timedelta("25:15"), timedelta(hours=25, minutes=15))
        self.assertEqual(Settings._string_to_timedelta("0:7"), timedelta(hours=0, minutes=7))


if __name__ == '__main__':
    unittest.main()
