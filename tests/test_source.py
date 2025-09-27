import unittest
from sources import source


class TestSource(source.Source):
    def __init__(self, settings):
        super(TestSource, self).__init__(settings)
        self.location_name = "Test_location"

    def update(self) -> None:
        self.calculate_dewpoint()


class MyTestCase(unittest.TestCase):

    def setUp(self):
        settings = {"nothing": "nothing"}
        self.test_source = TestSource(settings)

    def test_calculate_dewpoint(self):
        self.test_source.temperature = 70
        self.test_source.humidity = 50
        self.test_source.calculate_dewpoint()
        self.assertAlmostEqual(self.test_source.dewpoint, 50.5, 1)
        self.test_source.temperature = 70
        self.test_source.humidity = 0
        self.test_source.calculate_dewpoint()
        self.assertAlmostEqual(self.test_source.dewpoint, 0, 1)

    def test_get_state_dict(self):
        self.assertEqual(self.test_source.get_state_dict(), {'Test_location_aqi': 0, 'Test_location_temperature': 0, 'Test_location_humidity': 0, 'Test_location_wind': 0, 'Test_location_pressure': 0, 'Test_location_dewpoint': 0, 'Test_location_daily_high': 0})


if __name__ == '__main__':
    unittest.main()
