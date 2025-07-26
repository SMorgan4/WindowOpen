import requests
from sources import source


class OpenWeatherMap(source.Source):
    def __init__(self, settings):
        super(OpenWeatherMap, self).__init__(settings)
        self.latitude = settings.latitude
        self.longitude = settings.longitude
        self.key = settings.open_weather_map_id
        self.units = settings.units
        self.location_name = "outdoors"

    def __str__(self):
        return self.location_name + "\n" \
            f'Aqi: {self.aqi}\n' \
            f'Temperature: {self.temperature}\n' \
            f'Humidity: {self.humidity}\n' \
            f'Wind: {self.wind}\n' \
            f'Clouds: {self.clouds}'

    def update(self):
        self._get_weather()
        self._get_pollution()
        self.calculate_dewpoint()

    def _get_weather(self) -> None:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?",
                                params={'lat': self.latitude,
                                        'lon': self.longitude,
                                        'units': self.units,
                                        'appid': self.key})
        if response.status_code == 200:
            weather = response.json()
            self.temperature = weather['main']['temp']
            self.humidity = weather['main']['humidity']
            self.wind = weather['wind']['speed']
            self.clouds = weather['clouds']['all']
            self.high = weather["main"]["temp_max"]

    def _get_pollution(self) -> None:
        response = requests.get("http://api.openweathermap.org/data/2.5/air_pollution?",
                                params={'lat': self.latitude, 'lon': self.longitude, 'appid': self.key})
        if response.status_code == 200:
            outdoor_aqi = response.json()
            self.aqi = outdoor_aqi['list'][0]["main"]['aqi']