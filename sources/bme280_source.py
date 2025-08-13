import smbus2
import bme280
from sources import source


class BME280Source(source.Source):
    """Wrapper class for BME280 so that it can be used as a source"""
    def __init__(self, settings):
        super(BME280Source, self).__init__(settings)
        port = 1
        address = 0x77  # This could also be 0x76. This should probably be made configurable
        bus = smbus2.SMBus(port)

        calibration_params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, calibration_params)

        self.location_name = "Indoors"

    def update(self):
        self.temperature = self.c_to_f(self.bme280.temperature)
        self.humidity = self.bme280.humidity
        self.pressure = self.bme280.pressure
        self.calculate_dewpoint()

    def __str__(self):
        return self.location_name + '\n' \
            f'Temperature: {self.temperature}\n' \
            f'Humidity: {self.humidity}\n' \
            f'Pressure: {self.pressure}'

