import unittest
from sources import source


class TestSource(source.Source):
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


if __name__ == '__main__':
    unittest.main()
