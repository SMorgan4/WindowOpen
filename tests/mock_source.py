from sources import source


class MockSource(source.Source):
    """Source for testing without dependencies"""
    def __init__(self, settings):
        super(MockSource, self).__init__(settings)
        self.location_name = "Test"

    def update(self):
        self.calculate_dewpoint()

    def __str__(self):
        return self.location_name + '\n' \
                f'Temperature: {self.temperature}\n' \
                f'Humidity: {self.humidity}\n' \
                f'Pressure: {self.pressure}'
