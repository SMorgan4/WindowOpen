from sources import bme280_source
from sources import open_meteo_source
from program_settings import Settings
import schedule
from datetime import datetime
import time
from notifier import Notifier


class WindowOpen:

    def __init__(self):
        self.settings = Settings('config.json')
        self.weather_source = open_meteo_source.OpenMeteo(self.settings)
        self.indoor_source = bme280_source.BME280Source(self.settings)
        self._setup_schedule()
        self.notifier = Notifier(self.indoor_source, self.weather_source)

    def check_and_notify(self, check_mode, run_once: bool = False):
        if self.should_open(check_mode):
            self.notifier.send_open_request()
        if run_once:
            return schedule.CancelJob

    def should_open(self, check_mode) -> bool:
        """ Checks current conditions. Returns True if windows should be opened"""
        self.weather_source.update()
        self.indoor_source.update()
        if check_mode == "morning":
            if self.weather_source.daily_high < self.settings.forecast_temp_threshold:
                return False
        elif check_mode == "evening":
            if self._reschedule_evening():
                print("fail at reschedule")
                return False
            if self.indoor_source.temperature <= self.settings.max_desired_indoor_temp:
                return False
        if not self._shared_checks():
            return False
        return True

    def _reschedule_evening(self) -> bool:
        """Returns true if we should reschedule, ie, if the temp diff is too small, or we are past the max opening time"""
        if self.indoor_source.temperature - self.settings.min_temp_diff <= self.weather_source.temperature:
            return False
        if (datetime.now() > datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
                + self.settings.evening_end_time):
            return False
        schedule.every(1).hour.do(self.check_and_notify, check_mode="evening", run_once=True)
        return True

    def _shared_checks(self) -> bool:
        """Runs checks that are used in both morning and evening style checks"""
        if self.weather_source.wind > self.settings.max_wind:
            return False
        if self.weather_source.aqi > self.settings.max_aqi:
            return False
        if self.indoor_source.temperature < self.settings.min_indoor_temp:
            return False
        if ((self.weather_source.humidity > self.settings.max_outdoor_humidity) and
                (self.weather_source.dewpoint > self.indoor_source.dewpoint)):
            return False
        if self.indoor_source.temperature - self.settings.min_temp_diff <= self.weather_source.temperature:
            return False
        return True

    def _setup_schedule(self):

        # I don't think I need to save these. If live updates are req. we can use schedule.clear() and then re-run
        # this with the new data
        evening_time = str(self.settings.evening_start_time).zfill(8)
        morning_time = str(self.settings.weekday_morning_time).zfill(8)
        #evening check
        schedule.every().days.at(evening_time).do(self.check_and_notify, check_mode="evening")
        #weekday morning checks
        schedule.every().monday.at(morning_time).do(self.check_and_notify, check_mode="morning")
        schedule.every().tuesday.at(morning_time).do(self.check_and_notify, check_mode="morning")
        schedule.every().wednesday.at(morning_time).do(self.check_and_notify, check_mode="morning")
        schedule.every().thursday.at(morning_time).do(self.check_and_notify, check_mode="morning")
        schedule.every().friday.at(morning_time).do(self.check_and_notify, check_mode="morning")

    @staticmethod
    def run_schedule_loop():
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    checker = WindowOpen
    checker.run_schedule_loop()



