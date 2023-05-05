import speech_recognition as sr
import pyttsx3
import vosk
import os
import wave
import json
import traceback
import user

import assistant


class AudioProcessor:
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
    def use_offline_recognition(self, audio, language="russian"):

        # запишем аудио в файл для перевода в текст через vosk
        with open("microphone-results.wav", "wb") as file:
            file.write(audio.get_wav_data())

        recognized_data = ""
        try:
            # проверка наличия модели на нужном языке в каталоге приложения

            # Необходимо ввести путь к местоположению модуля распознавания воск!!!!!!1
            model_path = ""

            if (language == "russian"):
                model_path = "models/vosk-model-small-ru-0.22"  # путь к файлу модели
            elif (language == "english"):
                model_path = "models/vosk-model-en-us-0.22-lgraph"  # путь к файлу модели

            if not os.path.exists(model_path):
                print("Please download the model from:\n"
                      "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
                exit(1)


            # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
            wave_audio_file = wave.open("microphone-results.wav", "rb")
            model = vosk.Model(model_path)
            rec = vosk.KaldiRecognizer(model, wave_audio_file.getframerate())

            data = wave_audio_file.readframes(wave_audio_file.getnframes())

            last_n = True

            while last_n:
                last_n = False
                if len(data) > 0:
                    if rec.AcceptWaveform(data):
                        # получение данных распознанного текста из JSON-строки (чтобы можно было выдать по ней ответ)
                        res = json.loads(rec.Result())

                        if res['text'] != '':
                            recognized_data += f" {res['text']}"
                            last_n = False
                        elif not last_n:
                            recognized_data += '\n'
                            last_n = True

            res = json.loads(rec.FinalResult())
            recognized_data += f" {res['text']}"

        except:
            traceback.print_exc()
            print("Sorry, speech service is unavailable. Try again later")

        return recognized_data

    def audio_to_text(self, audio, language):
        # функция перевода аудио в текст

        # запишем аудио в файл для перевода в текст через vosk
        with open("microphone-results.wav", "wb") as file:
            file.write(audio.get_wav_data())

    def audio_to_text(self, audio):


        try:
            text = self.recognizer.recognize_google(audio, language="ru-Ru")
            return str(text)
        except sr.RequestError:
            print("распознавание через Vosk:")
            try:
                text = self.use_offline_recognition(audio, language)
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

