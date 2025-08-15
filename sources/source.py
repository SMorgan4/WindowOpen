from abc import ABC, abstractmethod
import psychrolib
import logging


class Source(ABC):
    @abstractmethod
    def update(self) -> None:
        pass

    def __init__(self, settings):
        self.aqi = 0
        self.temperature = 0
        self.humidity = 0
        self.wind = 0
        self.pressure = 0
        self.dewpoint = 0
        self.daily_high = 0
        self.logger = logging.getLogger(__name__)
        psychrolib.SetUnitSystem(psychrolib.IP)

    def calculate_dewpoint(self) -> None:
        if self.humidity != 0:
            self.dewpoint = psychrolib.GetTDewPointFromRelHum(self.temperature, self.humidity / 100)
        else:
            self.dewpoint = 0

    @staticmethod
    #TODO update tests to use metric values for indoor temps
    def c_to_f(temp) -> float:
        return (temp * 9/5) + 32
