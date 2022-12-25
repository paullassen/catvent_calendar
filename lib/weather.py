from os import path
from datetime import date

import requests

class Weather:
    def __init__(self, city, units):
        self.city = "&q=" + city
        self.units = "&units=" + units
        self.api_key = "appid=" + self.get_api_key()

        self.weather_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.geocode_url = "https://api.openweathermap.org/geo/1.0/direct?"

        self.lat = ''
        self.lon = ''
        self.weather_desc = ''
        self.temp = 0
        self.today = date.today()

        self.update_weather()


    def get_api_key(self):
        with open(path.dirname(path.abspath(__file__)) + '/../cfg/.owm_api_key', 'r') as f:
            key = f.read()
            return key[:-1]

    def get_lat_lon(self):
        url = self.geocode_url + self.api_key + self.city
        r = requests.get(url, timeout=10)
        data = r.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        return "&lat=" + str(lat), "&lon=" + str(lon)

    def update_weather(self):
        try:
            self.lat, self.lon = self.get_lat_lon()
        except:
            return

        url = self.weather_url + self.api_key + self.lat + self.lon + self.units
        r = requests.get(url, timeout=10)
        try:
            data = r.json()

            self.weather_desc = data['weather'][0]['description']
            self.temp = data['main']['temp']
            self.today = date.today()
        except:
            pass

    def get_weather(self):
        return self.weather_desc

    def get_temp(self):
        return self.temp

    def get_date(self):
        return self.today

if __name__ == "__main__":
    import sys
    w = Weather(sys.argv[1], "imperial")
    data = w.get_weather()
    print(f'Today is {w.get_date()}, the weather is {data} and the temperature is {w.get_temp()}')


 

