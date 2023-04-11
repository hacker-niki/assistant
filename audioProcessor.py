import speech_recognition as sr
import pyttsx3


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
            return text
        except sr.RequestError:
            print("Что-то с интернетом(( Проверьте подключение, пожалуйста")
        except sr.UnknownValueError:
            print("Не расслышал, что Вы сказали. Повторите")

    def answer_text_to_audio(self, text):
        # функция воспроизведения текста
        self.engine.say(text)
        self.engine.runAndWait()
