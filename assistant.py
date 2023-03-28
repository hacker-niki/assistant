import pyttsx3
import speech_recognition as sr
import datetime
from functions import extract_city
from functions import get_weather


class Assistant:
    def __init__(self):
        # Создаем объект для синтеза речи
        self.engine = pyttsx3.init()

        # Устанавливаем голос для синтеза речи
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

        self.speak("Здарова, Меченый!")

    def run(self):
        # Главный цикл программы
        while True:
            command = self.recognize_speech()
            if self.process_command(command):
                break

    # Функция для воспроизведения речи
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # Функция для распознавания речи

    def recognize_speech(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Говорите...")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='ru-RU')
                print("Вы сказали: {}".format(text))
                return text
            except:
                print("Не удалось распознать речь")
                return ""

    # Функция для выполнения команд
    def process_command(self, command):
        if "привет" in command.lower():
            self.speak("Хабар принес?")
        elif "как дела" in command.lower():
            self.speak("Можно и передохнуть маленько")
        elif "который час" in command.lower():
            now = datetime.datetime.now()
            self.speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
        elif extract_city(command) is not None:
            self.speak(get_weather(extract_city(command)))
            # print("погода")
        elif "стоп" in command.lower():
            self.speak("Ну, удачной охоты, сталкер.")
            return True
        self.speak("Иди своей дорогой, сталкер!")
        return False
