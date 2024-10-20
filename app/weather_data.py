import requests
import time
import json
import os

API_KEY = os.getenv('API_KEY')

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'main': data['weather'][0]['main'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'dt': data['dt']
        }
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

def fetch_weather_data(cities):
    weather_data = {}
    for city in cities:
        weather_data[city] = get_weather(city)
    return weather_data
