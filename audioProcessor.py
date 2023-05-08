import speech_recognition
import speech_recognition as sr
import pyttsx3
import vosk
import os
import wave
import json
import traceback
import user

import assistant
from pvrecorder import PvRecorder


class AudioProcessor:

    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            # проверка наличия модели на нужном языке в каталоге приложения
            if not os.path.exists("data\\vosk-model-small-ru-0.22"):
                print(("Please download the model from:\n"
                       "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.",
                       "red"))

                # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
            self.model = vosk.Model("data\\vosk-model-small-ru-0.22")

            self.microphone = speech_recognition.Microphone()
            with self.microphone:
                self.recognizer.adjust_for_ambient_noise(self.microphone, duration=1)

        except:
            traceback.print_exc()
            print(("Sorry, speech service is unavailable. Try again later", "red"))
            exit(1)

    def record_and_recognize_audio(self):
        with self.microphone:
            recognized_data = ""
            # регулирование уровня окружающего шума
            try:
                print("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 6)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                return ("Я ничего не услышал")

            # использование online-распознавания через Google
            # (высокое качество распознавания)
            try:
                print("Started recognition...")
                # print("Trying to use offline recognition...")
                recognized_data = self.use_offline_recognition()
            except:
                print("Unable to recognize")
                exit(1)
        print(recognized_data)
        return recognized_data

    def use_offline_recognition(self):

        recognized_data = ""

        wave_audio_file = wave.open("microphone-results.wav", "rb")

        offline_recognizer = vosk.KaldiRecognizer(self.model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                # получение данных распознанного текста из JSON-строки (чтобы можно было выдать по ней ответ)
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]

        return recognized_data

    # def audio_to_text(self, audio, language):
    #     # функция перевода аудио в текст
    #
    #     # запишем аудио в файл для перевода в текст через vosk
    #     with open("microphone-results.wav", "wb") as file:
    #         file.write(audio.get_wav_data())

    def audio_to_text(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language="ru-Ru")
            return str(text)
        except sr.RequestError:
            print("распознавание через Vosk:")
            try:
                text = self.use_offline_recognition()
                # print(text)
                return str(text)
            except sr.UnknownValueError:
                print("Не расслышал, что Вы сказали. Повторите")
                return ""
        except sr.UnknownValueError:
            print("Не расслышал, что Вы сказали. Повторите")
            return ""

    def answer_text_to_audio(self, text):
        # функция воспроизведения текста
        self.engine.say(text)
        self.engine.runAndWait()
