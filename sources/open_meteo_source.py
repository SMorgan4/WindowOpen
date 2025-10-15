import requests
from sources import source
from datetime import datetime


class OpenMeteo(source.Source):
    def __init__(self, settings):
        super(OpenMeteo, self).__init__(settings)
        self.latitude = settings.latitude
        self.longitude = settings.longitude
        self.units = settings.units
        self.time_zone = settings.time_zone
        self.location_name = "outdoors"
        self.forecast_days = 1
        self.wind_speed_unit = "mph"
        self.temperature_unit = "fahrenheit"
        self.precipitation_unit = "inch"

    def __str__(self):
        return self.location_name + "\n" \
            f'Aqi: {self.aqi}\n' \
            f'Temperature: {self.temperature}\n' \
            f'Humidity: {self.humidity}\n' \
            f'Wind: {self.wind}\n'\
            f'Daily high: {self.daily_high}\n'\
            f'Solar irradiance:{self.irradiance}\n'

    def update(self):
        self._get_weather()
        self._get_pollution()
        self.calculate_dewpoint()

    def _get_weather(self) -> None:
        response = requests.get("https://api.open-meteo.com/v1/forecast?",
                                params={'latitude': self.latitude,
                                        'longitude': self.longitude,
                                        'daily': "temperature_2m_max",
                                        'hourly': "direct_normal_irradiance",
                                        'current': "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_gusts_10m",
                                        'timezone': self.time_zone,
                                        'forcast_days': self.forecast_days,
                                        'wind_speed_unit': self.wind_speed_unit,
                                        'temperature_unit': self.temperature_unit,
                                        'precipitation_unit': self.precipitation_unit})
        if response.status_code == 200:
            weather = response.json()
            self.temperature = weather['current']['temperature_2m']
            self.humidity = weather['current']['relative_humidity_2m']
            self.wind = weather['current']['wind_speed_10m']
            self.daily_high = weather["daily"]["temperature_2m_max"][0]
            self.irradiance = self.get_param_at_present(weather["hourly"]["direct_normal_irradiance"])
        else:
            self.logger.error("Error fetching weather")
            self.logger.error(response.status_code)

    @staticmethod
    def get_param_at_present(values: list):
        return values[datetime.now().hour]

    def _get_pollution(self) -> None:
        response = requests.get("https://air-quality-api.open-meteo.com/v1/air-quality?",
                                params={'latitude': self.latitude,
                                        'longitude': self.longitude,
                                        'current': 'us_aqi',
                                        'timezone': self.time_zone,
                                        'forecast_days': self.forecast_days})
        if response.status_code == 200:
            outdoor_aqi = response.json()
            self.aqi = outdoor_aqi['current']["us_aqi"]
        else:
            self.logger.error("Error fetching pollution")
            self.logger.error(response.status_code)
