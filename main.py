from sources import bme280_source
from sources import open_meteo_source
from program_settings import Settings
import schedule
from datetime import datetime
import time
from notifier import Notifier
import logging
from history import write_row


class WindowOpen:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='windowOpen.log', encoding='utf-8', level=logging.WARNING,
                            format='%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
        self.logger.info("Setting up")
        self.settings = Settings('config.json')
        self.weather_source = open_meteo_source.OpenMeteo(self.settings)
        self.indoor_source = bme280_source.BME280Source(self.settings)
        self.source_list = [self.indoor_source, self.weather_source]
        self._setup_schedule()
        self.notifier = Notifier(self.indoor_source, self.weather_source)
        self.logger.info("Finished setup")

    def check_and_notify(self, check_mode, run_once: bool = False):
        self.logger.info("Checking current conditions")
        if self.should_open(check_mode):
            self.logger.info("Sending Open request")
            self.notifier.send_open_request()
        if run_once:
            self.logger.info("Additional check completed")
            return schedule.CancelJob

    def should_open(self, check_mode) -> bool:
        """ Checks current conditions. Returns True if windows should be opened"""
        self.weather_source.update()
        self.logger.info("Updated indoor source:")
        self.logger.info(str(self.indoor_source))
        self.indoor_source.update()
        self.logger.info("Updated outdoor source:")
        self.logger.info(str(self.weather_source))

        if check_mode == "morning":
            if self.weather_source.daily_high < self.settings.forecast_temp_threshold:
                self.logger.info("Check failed - forecast not hot enough.")
                return False
        elif check_mode == "evening":
            if self.indoor_source.temperature <= self.settings.max_desired_indoor_temp:
                self.logger.info("Check failed - not hot enough inside")
                return False
        if not self._shared_checks():
            if check_mode == "evening":
                self._reschedule_evening()
            return False
        return True

    def _reschedule_evening(self) -> bool:
        """Returns true and reschedules if we are within the re-scheduling window"""
        if (datetime.now() > datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
                + self.settings.evening_end_time):
            return False
        self.logger.info("Scheduling additional check")
        schedule.every(self.settings.retry_interval).minutes.do(self.check_and_notify, check_mode="evening", run_once=True)
        return True

    def _shared_checks(self) -> bool:
        """Runs checks that are used in both morning and evening style checks"""
        if self.weather_source.wind > self.settings.max_wind:
            self.logger.info("Check failed - too windy")
            return False
        if self.weather_source.aqi > self.settings.max_aqi:
            self.logger.info("Check failed - air quality")
            return False
        if self.indoor_source.temperature < self.settings.min_indoor_temp:
            self.logger.info("CHeck failed - too cold inside.")
            return False
        if ((self.weather_source.humidity > self.settings.max_outdoor_humidity) and
                (self.weather_source.dewpoint > self.indoor_source.dewpoint)):
            self.logger.info("Check failed - too humid outside.")
            return False
        if self.indoor_source.temperature - self.settings.min_temp_diff <= self.weather_source.temperature:
            self.logger.info("Check failed - min temp differential not met.")
            return False
        return True

    def _setup_schedule(self):

        # I don't think I need to save these. If live updates are req. we can use schedule.clear() and then re-run
        # this with the new data
        self.logger.info("Creating schedule")
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

        schedule.every().hour.at(":00").do(write_row, self.source_list)
        self.logger.info("Schedule created")

    def run_schedule_loop(self):
        self.logger.info("Started running schedule")
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    checker = WindowOpen()
    checker.run_schedule_loop()


if __name__ == "__main__":
    main()
