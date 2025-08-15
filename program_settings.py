import json
from os import path
from datetime import timedelta
import logging


class Settings:
    def __init__(self, setting_file):
        self.logger = logging.getLogger(__name__)
        self.setting_file = path.join(path.dirname(path.abspath(__file__)), setting_file)
        if path.exists(self.setting_file):
            with open(self.setting_file, "r") as infile:
                setting_data = json.load(infile)
                self.latitude = setting_data["latitude"]
                self.longitude = setting_data["longitude"]
                self.units = setting_data["units"]

                # The below is the min forecast temperature required for the program to recommend opening windows in
                # the morning
                self.forecast_temp_threshold = setting_data["forecast_temp_threshold"]
                self.max_wind = setting_data["max_wind"]
                self.max_aqi = setting_data["max_aqi"]
                self.min_indoor_temp = setting_data["min_indoor_temp"]
                self.max_outdoor_humidity = setting_data["max_outdoor_humidity"]
                self.max_desired_indoor_temp = setting_data["max_desired_indoor_temp"]
                self.min_temp_diff = setting_data["min_temp_diff"]
                self.time_zone = setting_data["time_zone"]

                self.evening_start_time = self._string_to_timedelta(setting_data["evening_start_time"])
                self.evening_end_time = self._string_to_timedelta(setting_data["evening_end_time"])
                self.weekday_morning_time = self._string_to_timedelta(setting_data["weekday_morning_time"])

        else:
            self.logger.error("Error config file not found")

    @staticmethod
    def _string_to_timedelta(str_time: str) -> timedelta:
        """ Time must be in HH:MM or H:MM format. Leading zero req."""
        #TODO add regex? to enforce the above
        parts = str_time.split(':')
        return timedelta(hours=float(parts[0]), minutes=float(parts[1]))