import unittest
from sources import open_meteo_source
from program_settings import Settings


class TestOpenMeteoSource(unittest.TestCase):
    def test_something(self):
        settings = Settings('config.json')
        weather_source = open_meteo_source.OpenMeteo(settings)
        weather_source.update()
        print(weather_source)


if __name__ == '__main__':
    unittest.main()
