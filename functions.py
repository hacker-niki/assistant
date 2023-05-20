import datetime
import json
import os
import random
import re
import subprocess
import time
import webbrowser
from ctypes import cast, POINTER

import keyboard
import openai
import pyautogui as pg
import pybrightness
import requests
import speech_recognition as sr
from comtypes import CLSCTX_ALL
from fuzzywuzzy import fuzz
from googletrans import Translator
from num_to_rus import Converter
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from audioProcessor import AudioProcessor
from user import client


def changeNumberIntoLetter(value):
    number = numToLetter(value)
    return number


def numToLetter(value):  # The function converts the numbers into letters.
    if value == 1:
        return 'one'
    elif value == 2:
        return 'two'
    elif value == 3:
        return 'three'
    elif value == 4:
        return 'four'
    elif value == 5:
        return 'five'
    elif value == 6:
        return 'six'
    elif value == 7:
        return 'seven'
    elif value == 8:
        return 'eight'
    elif value == 9:
        return 'nine'
    elif value == 10:
        return 'ten'
    elif value == 11:
        return 'eleven'
    elif value == 12:
        return 'twelve'
    elif value == 13:
        return 'thirteen'
    elif 13 < value <= 19:
        return composeTeen(value)
    elif value > 19:
        if value == 20:
            return 'twenty'
        elif value == 30:
            return 'thirty'
        elif value == 50:
            return 'fifty'
        elif value == 10 ** 2:
            return 'one hundred'
        elif value == 10 ** 3:
            return 'one thousand'
        elif value == 10 ** 5:
            return 'one hundred thousand'
        elif value == 10 ** 6:
            return 'one milion'
        elif value >= 20:
            return composeNumbers(value)
        else:
            exit('Out of range')
    else:
        return ''


def composeNumbers(value):  # The function build every number biger than 40
    if 40 <= value < 10 ** 2:
        value1 = int(str(value)[0])
        value2 = int(str(value)[1])
        if value1 == 2:
            value1 = 'twen'
            return value1 + 'ty' + '-' + numToLetter(value2)
        if value1 == 3:
            value1 = 'thir'
            return value1 + 'ty' + '-' + numToLetter(value2)
        if value1 == 8:
            value1 = 'eigh'
            return value1 + 'ty' + '-' + numToLetter(value2)
        elif value1 == 5:
            value1 = 'fif'
            return value1 + 'ty' + '-' + numToLetter(value2)
        return numToLetter(value1) + 'ty' + '-' + numToLetter(value2)
    elif 10 ** 2 <= value < 10 ** 3:
        value1 = int(str(value)[0])
        value2 = int(str(value)[1:])
        return numToLetter(value1) + ' ' + 'hundred' + ' ' + numToLetter(value2)
    elif 10 ** 3 <= value < 10 ** 4:
        value1 = int(str(value)[0])
        value2 = int(str(value)[1:])
    elif 10 ** 4 <= value < 10 ** 5:
        value1 = int(str(value)[0:2])
        value2 = int(str(value)[2:])
    elif 10 ** 5 <= value < 10 ** 6:
        value1 = int(str(value)[0:3])
        value2 = int(str(value)[3:])
    return numToLetter(value1) + ' ' + 'thousand' + ' ' + numToLetter(value2)


def composeTeen(value):  # The function takes the unit and then converts it into letter to build the word.
    value = int(str(value)[
                    -1])  # It turns elem in string to take the last position and it converts it again in integer to change it in letters. Then it composes the word adding 'teen' at the end.
    value = numToLetter(value)
    if value == 'five': value = 'fif'
    value = value + 'teen'
    return value


def extract_city_function(command: str):
    pattern = r"погода в ([\w\s]+)"
    match = re.search(pattern, command.lower())
    if match:
        return match.group(1)
    else:
        return None


def weather_function(a):
    api_key = "d3b9ddd02bf307000417e311a213a7f4"  # Open Weather
    with open('data.json', 'r') as file:
        data = json.load(file)
        town = data['town']
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={town}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    translator = Translator()
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return translator.translate(text=
                                    f"In {town} {weather}, temperature {changeNumberIntoLetter(int(temperature))} degrees "
                                    f"celsius, humidity {changeNumberIntoLetter(int(humidity))} percents, and wind speed {changeNumberIntoLetter(int(wind_speed))}"
                                    f"meters per second.",
                                    dest="ru").text
    else:
        return "Извините, я не смог получить информацию о погоде в этом городе."


def hello_function(a) -> str:
    return "Хабар принес?"


def doing_function(a) -> str:
    return "Можно и передохнуть маленько"


def time_function(a) -> str:
    now = datetime.datetime.now()
    conv = Converter()
    return "Сейчас " + conv.convert(now.hour) + " часов " + conv.convert(now.minute) + " минут"


def stop_function(a) -> str:
    return "Ну, удачной охоты, сталкер."


def default_function(a) -> str:
    return "Не удалось распознать команду."


def spotify_function(a) -> str:
    sentence = ''.join(a)
    # открывает и ищет в Spotify через браузер
    url = "https://open.spotify.com/search/" + sentence
    webbrowser.get().open(url)
    return "Открываю спотифай"


def launch_desktop_spotify(a) -> str:
    # запуск десктопного приложения Spotify и запуск существующей песни
    sentence: str = ""
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


def mood_function(a) -> str:
    return "Какие дела могут быть у робота? Не крашнулся и то хорошо"


def joke_function(a) -> str:
    random_number = random.randint(0, 3)
    if random_number == 0:
        return "Если вы внезапно оказались в яме, первое, что нужно сделать - перестать копать!"
    elif random_number == 1:
        return "Штирлиц уходил от ответа, ответ неотступно следовал за ним."
    elif random_number == 2:
        return "Уходя из квартиры, делай селфи с утюгом! Так ты избежишь ненужных сомнений."
    elif random_number == 3:
        return "Колобок повесился, ахаххаха"


def commands_function(a) -> str:
    return "Пока что я могу: повторить за вами, настроить яркость и звук, выключить компьютер, изменить расскладку клавиатуры, подбросить монетку, рассказать или написать что-нибудь, найти информацию в интернете, рассказать прогноз погоды, найти видео в ютубе, рассказать анекдот, сказать сколько сейчас времени, найти определение в википедии, настроить данные о пользователе,  поприветсвовать вас, попрощаться с вами, найти песню в спотифай, также вы можете поинтересоваться как у меня дела"


def search_function(a) -> str:  # type: ignore
    sentence = ''.join(a)
    try:
        webbrowser.open_new_tab("https://www.google.com/search?q=" + sentence)
        return "Открываю браузер"
    except:
        return "Не удалось открыть браузер"


def youtube_function(a) -> str:
    # print(sentence)
    sentence = ''.join(a)
    url = "https://www.youtube.com/results?search_query=" + sentence
    try:
        webbrowser.get().open(url)
        return "Открываю ютуб"
    except:
        return "Не удалось открыть ютуб"


def wikipedia_function(query) -> str:
    sentence = ''.join(query)
    url = "https://ru.wikipedia.org/wiki/Special:Search?search=" + sentence
    try:
        webbrowser.get().open(url)
        return "Открываю Википедию"
    except:
        return "Не удалось открыть Википедию"


def settings_function(a) -> str:
    settings = AudioProcessor()

    settings.answer_text_to_audio(
        "Выберете что вы хотите поменять: имя, пол, основной язык, дополнительный язык, город")
    audio = recognize_speech()
    parametr = settings.audio_to_text(audio)

    if parametr == "имя":
        settings.answer_text_to_audio("Скажите как вас зовут")
        audio = recognize_speech()
        name = settings.audio_to_text(audio)
        client.name = name
    elif parametr == "пол":
        settings.answer_text_to_audio("Скажите какого вы пола")
        audio = recognize_speech()
        sex = settings.audio_to_text(audio)
        client.sex = sex
    elif parametr == "основной язык":
        settings.answer_text_to_audio("Каким будет ваш основной язык")
        audio = recognize_speech()
        language = settings.audio_to_text(audio)
        client.language = language
    elif parametr == "дополнительный язык":
        settings.answer_text_to_audio("Каким будет ваш дополнительный язык")
        audio = recognize_speech()
        second_language = settings.audio_to_text(audio)
        client.secondLanguage = second_language
    elif parametr == "город":
        settings.answer_text_to_audio("Каким будет ваш город")
        audio = recognize_speech()
        town = settings.audio_to_text(audio)
        client.town = town

    return "Изменения были успешно введены"


def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source, phrase_time_limit=5)
        return audio


def repeat_function(a) -> str:
    sentence = ''.join(a)
    repeat = AudioProcessor()
    repeat.answer_text_to_audio(sentence)
    return ""


# функция работает по типу яркость + число на которое надо установить текущюу яркость в процентах
def brightness_function(a) -> str:
    sentence = ' '.join(a)
    number = int(re.findall(r'\d+', sentence)[0] + re.findall(r'\d+', sentence)[1])
    pybrightness.custom(number)
    return ""


# оч опасная функция честно первый раз было оч страшно запускать
def off_function(a) -> str:
    subprocess.call('shutdown /s /t 2', shell=True)
    return ""


def key_board_function(a) -> str:
    keyboard.press_and_release('left alt + shift')
    return ""


def write_function_function(a) -> str:
    sentence = "напиши " + ''.join(a)
    settings = AudioProcessor()

    settings.answer_text_to_audio("Выполняю")
    print(sentence)
    openai.api_key = "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"
    model_engine = "text-davinci-002"
    openai.api_base = "https://api.openai.com/v1/"

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=sentence,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    generated_text = message.strip()
    try:
        answer = "Запрос: " + sentence + ' ' + generated_text
        with open("C:\\exe.win-amd64-3.10\\example.txt", 'w') as f:
            f.write(answer)
        os.system("C:\\exe.win-amd64-3.10\\example.txt")
        return "Задание выполнено"
    except:
        return "Задание не выполнено"


def say_function(a) -> str:
    sentence = "расскажи " + ''.join(a)
    print(sentence)
    openai.api_key = "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"
    model_engine = "text-davinci-002"
    openai.api_base = "https://api.openai.com/v1/"

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=sentence,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    generated_text = message.strip()

    return generated_text


def coin_function(a) -> str:
    random_number = random.randint(0, 1)
    if random_number == 0:
        return "Выпал орел"
    else:
        return "Выпала решка"


def sound_function(a) -> str:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    if current_volume == 0:
        new_volume = 0.5
    else:
        new_volume = 0
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    return ""


# Потестите плиз функцию у меня выдает оч странную ошибку
def translator_function(a) -> str:
    sentence = ''.join(a)
    translator = Translator()
    translation = translator.translate(sentence, dest='ru', src='en')
    return translation.text


def random_function(a) -> str:
    sentence = ''.join(a)
    print(sentence)
    pattern = r'\d+'
    matches = re.findall(pattern, sentence)
    numbers = [int(match) for match in matches]
    print(numbers)
    try:
        conv = Converter()
        random_number = random.randint(numbers[0], numbers[1])
        return conv.convert(random_number)
    except:
        return "Не удалось получить число"


def app_function(app_name) -> str:
    print(app_name)
    app_name = app_name.lower()
    program_files = ["C:/Program Files/", "C:/Program Files (x86)/"]

    def find_apps(root, app_name):
        best_score = 0
        best_match = None

        for path, dirs, files in os.walk(root):
            for file in files:
                if file.endswith('.exe'):
                    exe_name = file[:-4].lower()  # remove '.exe' and convert to lower case
                    folder_name = path.split(os.sep)[-1].lower()  # get the name of the folder

                    exe_score = fuzz.partial_ratio(app_name, exe_name)
                    folder_score = fuzz.partial_ratio(app_name, folder_name)

                    # combine the scores (you may use different weights)
                    total_score = 0.6 * exe_score + 0.4 * folder_score

                    if total_score > best_score:
                        best_score = total_score
                        best_match = os.path.join(path, file)

        return best_match

    best_match = None
    best_score = 0

    for directory in program_files:
        match = find_apps(directory, app_name)
        if match:
            score = fuzz.ratio(app_name, match)
            if score > best_score:
                best_score = score
                best_match = match

    if best_match:
        subprocess.call(best_match)
        return "Открываю."
    else:
        return "Приложение не найдено."
