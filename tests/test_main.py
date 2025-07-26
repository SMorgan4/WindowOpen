import unittest
import schedule
from main import WindowOpen
from mock_source import MockSource
from program_settings import Settings
from datetime import datetime, timedelta


class TestMain(unittest.TestCase):

    def setUp(self):
        self.main = WindowOpen()

        self.settings = Settings("config.json")
        self.main.indoor_source = MockSource(self.settings)
        self.main.weather_source = MockSource(self.settings)
        self.main.notifier.send_open_request = self.mock_send_open_request
        self.set_default_test_settings()

    def mock_send_open_request(self):
        pass

    def test_should_open_default(self):
        self.assertTrue(self.main.should_open("evening"))
        self.assertTrue(self.main.should_open("morning"))

    def test_should_open_wind(self):
        self.main.weather_source.wind = self.settings.max_wind + 1
        self.assertFalse(self.main.should_open("evening"))
        self.assertFalse(self.main.should_open("morning"))

    def test_should_open_aqi(self):
        self.main.weather_source.aqi = self.settings.max_aqi + 1
        self.assertFalse(self.main.should_open("evening"))
        self.assertFalse(self.main.should_open("morning"))

    def test_should_open_indoor_too_cold(self):
        self.main.indoor_source.temperature = self.settings.min_indoor_temp - 1
        self.assertFalse(self.main.should_open("evening"))
        self.assertFalse(self.main.should_open("morning"))

    def test_should_open_too_humid(self):
        self.main.weather_source.humidity = self.main.settings.max_outdoor_humidity + 1
        self.main.indoor_source.humidity = 0  # makes sure indoor dew point is below the outdoor dewpoint for this test
        self.assertFalse(self.main.should_open("evening"))
        self.assertFalse(self.main.should_open("morning"))

    def test_should_open_forecast(self):
        self.main.weather_source.daily_high = 84
        self.assertFalse(self.main.should_open("morning"))

    def test_should_open_max_temp(self):
        self.main.indoor_source.temperature = self.settings.max_desired_indoor_temp - 1
        self.assertFalse(self.main.should_open("evening"))

    def test_reschedule_evening_late(self):
        self.main.settings.evening_end_time = current_time_of_day() + timedelta(minutes=5)
        num_jobs_start = len(schedule.get_jobs())
        self.assertTrue(self.main._reschedule_evening())
        num_jobs_end = len(schedule.get_jobs())
        self.assertEqual(num_jobs_start + 1, num_jobs_end)

    def test_reschedule_evening_warm(self):
        self.main.weather_source.temperature = 75
        num_jobs_start = len(schedule.get_jobs())
        self.assertFalse(self.main._reschedule_evening())
        num_jobs_end = len(schedule.get_jobs())
        self.assertEqual(num_jobs_start, num_jobs_end)

    def test_reschedule_evening_good(self):
        num_jobs_start = len(schedule.get_jobs())
        self.assertFalse(self.main._reschedule_evening())
        num_jobs_end = len(schedule.get_jobs())
        self.assertEqual(num_jobs_start, num_jobs_end)

    def set_default_test_settings(self):
        # Standard parameters that should result in a window opening recommendation
        self.main.indoor_source.temperature = 77
        self.main.indoor_source.humidity = 45
        self.main.weather_source.temperature = 65
        self.main.weather_source.humidity = 50
        self.main.weather_source.wind = 0
        self.main.weather_source.daily_high = 85
        self.main.weather_source.aqi = 10
        self.main.settings.min_temp_diff = 5
        self.main.settings.forecast_temp_threshold = 85
        # The above combination of parameters has a lower outside dewpoint than inside
        self.main.settings.evening_end_time = current_time_of_day() + timedelta(minutes=-5)


def current_time_of_day() -> timedelta:
    return (datetime(year=1, month=1, day=1, hour=datetime.now().hour, minute=datetime.now().minute) -
            datetime(year=1, month=1, day=1, hour=0, minute=0))


if __name__ == '__main__':
    unittest.main()
