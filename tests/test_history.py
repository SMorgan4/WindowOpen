import unittest
import history
from tempfile import mkstemp
import os
import csv
from mock_source import MockSource
from program_settings import Settings


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.test_file, self.test_file_path = mkstemp(suffix=".csv")
        os.close(self.test_file)
        settings = Settings("config.json")
        source_1 = MockSource(settings)
        source_2 = MockSource(settings)
        source_1.location_name = "location_1"
        source_2.location_name = "location_2"
        self.source_list = [source_1, source_2]

    def test_write_row(self):
        history.write_row(self.source_list, self.test_file_path)
        history.write_row(self.source_list, self.test_file_path)

        with open(self.test_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            print(next(reader))
            print(next(reader))
            print(next(reader))
            file.close()

    def tearDown(self):
        os.remove(self.test_file_path)


if __name__ == '__main__':
    unittest.main()
