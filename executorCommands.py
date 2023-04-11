import speech_recognition as sr
import requests


def check_internet():
    url = "https://www.google.com"
    timeout = 80
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        pass
    return False


class Recognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def execute(self):
        if check_internet():
            # Используем Google Speech Recognition
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
        else:
            # Используем Vosk
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_vosk(audio, )

        return text
