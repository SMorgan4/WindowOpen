from abc import ABC, abstractmethod
import psychrolib


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
        psychrolib.SetUnitSystem(psychrolib.IP)

    def calculate_dewpoint(self) -> None:
        if self.humidity != 0:
            self.dewpoint = psychrolib.GetTDewPointFromRelHum(self.temperature, self.humidity / 100)
        else:
            self.dewpoint = 0
