import speech_recognition as sr
import pyttsx3


<<<<<<< HEAD:AudioProcessor.py
class AudioProcessor():
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def audio_to_text(self, audio):
        # функция перевода текстa в аудио

        try:
            text = self.recognizer.recognize_google(audio, language="ru-Ru")
=======
class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[2].id)

    def audio_to_text(self, audio):
        # функция перевода текстa в аудио
        try:
            text = self.recognizer.recognize_google(audio, language="ru-Ru").lower()
>>>>>>> 4f883dea4867365920cf61f2d1053ec5f962d0ff:audioProcessor.py
            return text
        except sr.RequestError:
            print("Что-то с интернетом(( Проверьте подключение, пожалуйста")
            return ""
        except sr.UnknownValueError:
            print("Не расслышал, что Вы сказали. Повторите")
            return ""

    def answer_text_to_audio(self, text):
        # функция воспроизведения текста
        self.engine.say(text)
        self.engine.runAndWait()
