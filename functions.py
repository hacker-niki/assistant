import datetime
import re
import requests
import time
from googletrans import Translator, constants
import pyautogui as pg
import keyboard
import webbrowser
from playsound import playsound


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


def hello_function(a) -> str:
    return "Хабар принес?"


def doing_function(a) -> str:
    return "Можно и передохнуть маленько"


def time_function(a) -> str:
    now = datetime.datetime.now()
    return "Сейчас " + str(now.hour) + ":" + str(now.minute)


def stop_function(a) -> str:
    return "Ну, удачной охоты, сталкер."


def default_function(a) -> str:
    return "Не удалось распознать команду."

def spotify_function(a)->str:
    #открывает и ищет в Spotify через браузер
    sentence: str = ""
    for i in a:
        sentence += i
    print(sentence)
    url = "https://open.spotify.com/search/" + sentence
    webbrowser.get().open(url)
    time.sleep(2)

def launch_desktop_spotify(a)->str:
    #запуск десктопного приложения Spotify и запуск существующей песни
    sentence:str = ""
    for i in a:
        sentence += i
    print(sentence)
    pg.moveTo(250, 1050)
    pg.click()
    time.sleep(1)
    try:
        keyboard.write("spotify")
        keyboard.send("enter")
        time.sleep(3)
        keyboard.press(" ")
        return "Открываю спотифай"
    except FileNotFoundError:
        return "Не удалось открыть, пробую открыть через браузер"


def find_inf_in_Chrome(a)->str:
    #Функция поиска в Google Chrome
    sentence:str = ""
    for i in a:
        if(i==' '):
            i='+'
        sentence += i
    print(sentence)
    url = "https://google.com/?q=" + sentence
    try:
        webbrowser.get().open(url)
        time.sleep(2)
        keyboard.send("enter")
        return "Выполняю поиск"
    except:
        return "Не удалось открыть браузер"




