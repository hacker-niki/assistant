import datetime
import re
import requests
from googletrans import Translator, constants


def extract_city_function(command: str):
    pattern = r"погода в ([\w\s]+)"
    match = re.search(pattern, command.lower())
    if match:
        return match.group(1)
    else:
        return None


def get_weather_function(city: str):
    translator = Translator()
    result = translator.translate(city, src='ru', dest='en')
    api_key = "d3b9ddd02bf307000417e311a213a7f4"  # замените на свой API ключ OpenWeatherMap
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={result.text}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return translator.translate(
            f"In {city} {weather}, temperature {int(temperature)} degrees celsius, humidity {int(humidity)} percents, and wind speed {int(wind_speed)} meters per second.",
            dest="ru").text
    else:
        return "Извините, я не смог получить информацию о погоде в этом городе."


def hello_function() -> str:
    return "Хабар принес?"


def doing_function() -> str:
    return "Можно и передохнуть маленько"


def time_function() -> str:
    now = datetime.datetime.now()
    return "Сейчас " + str(now.hour) + ":" + str(now.minute)


def stop_function() -> str:
    return "Ну, удачной охоты, сталкер."
