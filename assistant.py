import pyttsx3
import speech_recognition as sr
import TextHandler


class Assistant:
    def __init__(self):
        # Создаем объект для синтеза речи
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[2].id)

        self.speak("Здарова, Меченый!")

    def run(self):
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
                print(f"Вы сказали: {format(text)}")
                return text
            except:
                print("Не удалось распознать речь")
                return ""

    # Функция для выполнения команд
    def process_command(self, command):

        return False
