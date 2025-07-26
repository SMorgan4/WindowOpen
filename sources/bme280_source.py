import board
from adafruit_bme280 import basic as adafruit_bme280
from sources import source


class BME280Source(source.Source):
    """Wrapper class for BME280 so that it can be used as a source"""
    def __init__(self, settings):
        super(BME280Source, self).__init__(settings)
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        self.location_name = "Indoors"

    def update(self):
        self.temperature = self.bme280.temperature
        self.humidity = self.bme280.humidity
        self.pressure = self.bme280.pressure
        self.calculate_dewpoint()

    def __str__(self):
        return self.location_name + '\n' \
                f'Temperature: {self.temperature}\n' \
                f'Humidity: {self.humidity}\n' \
                f'Pressure: {self.pressure}'
