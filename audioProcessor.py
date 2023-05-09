import speech_recognition as sr
import pyttsx3
import traceback
from sys import exit


class AudioProcessor:

    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()

            print(sr.Microphone.list_working_microphones())
            self.microphone = sr.Microphone()
            with self.microphone:
                self.recognizer.adjust_for_ambient_noise(self.microphone, duration=1)

        except:
            traceback.print_exc()
            print(("Sorry, speech service is unavailable. Try again later", "red"))
            exit(1)

    def record_and_recognize_audio(self):
        with self.microphone:
            try:
                print("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 6)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                return ("Я ничего не услышал")
            try:
                print("Started recognition...")
                recognized_data = self.audio_to_text(audio)
            except:
                print("Unable to recognize")
                exit(1)
        # print(recognized_data)
        return recognized_data

    def audio_to_text(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            return str(text)
        except sr.RequestError:
            print("Не удалось подключиться к сервису распознавания речи Google")
            return ""
        except sr.UnknownValueError:
            print("Не расслышал, что Вы сказали. Повторите")
            return ""

    def answer_text_to_audio(self, text):
        # функция воспроизведения текста
        self.engine.say(text)
        self.engine.runAndWait()
