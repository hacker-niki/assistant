import re
import requests
# from translate import Translator
from googletrans import Translator, constants


def extract_city(command: str):
    # задаем регулярное выражение для поиска города
    pattern = r"погода в ([\w\s]+)"
    # применяем регулярное выражение к команде пользователя
    match = re.search(pattern, command.lower())
    # если найдено совпадение, возвращаем название города
    if match:
        return match.group(1)
    # если совпадений нет, возвращаем None
    else:
        return None


def get_weather(city: str):
    translator = Translator()
    result = translator.translate("город", src='ru', dest='en')
    api_key = "d3b9ddd02bf307000417e311a213a7f4"  # замените на свой API ключ OpenWeatherMap
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={result.text}&appid={api_key}&units=metric"
    # print(translator.translate(city).text)
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
