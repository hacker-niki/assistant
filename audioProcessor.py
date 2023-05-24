import json
import multiprocessing
import os
import traceback

import pyttsx3
import speech_recognition as sr
import torch
import torch.package
from googletrans import Translator
from pydub import AudioSegment
from pydub.playback import play


class AudioProcessor:

    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
            torch.set_num_threads(4)
            russian_tts = 'data/model_ru.pt'
            english_tts = 'data/model_en.pt'
            with open('data.json', 'r') as file:
                data = json.load(file)
                key = data['language']
                print(key)
                if key == 'rus':
                    tts = russian_tts
                    self.lang = 'rus'
                else:
                    tts = english_tts
                    self.lang = 'eng'
                    self.translator = Translator()
            if not os.path.isfile(russian_tts):
                torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                               russian_tts)
            if not os.path.isfile(english_tts):
                torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt',
                                               english_tts)
            self.model = torch.package.PackageImporter(tts).load_pickle("tts_models", "model")
            self.model.to(device)
            self.microphone = sr.Microphone()
            with self.microphone:
                self.recognizer.adjust_for_ambient_noise(self.microphone, duration=1)

        except:
            traceback.print_exc()
            print("Sorry, speech service is unavailable. Try again later")

    def record_and_recognize_audio(self):
        with self.microphone:
            try:
                print("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 6)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                return "Я ничего не услышал"
            try:
                print("Started recognition...")
                recognized_data = self.audio_to_text(audio)
            except:
                print("Unable to recognize")
                return "Невозможно распознать речь"
        return recognized_data

    def audio_to_text(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            return str(text)
        except sr.RequestError:
            print("Не удалось подключиться к сервису распознавания речи Google")
            return "Не удалось подключиться к сервису распознавания речи Google"
        except sr.UnknownValueError:
            print("Не расслышал, что Вы сказали. Повторите")
            return "Не расслышал, что Вы сказали. Повторите"

    def run_audio(self, audio_paths):
        play(AudioSegment.from_file(audio_paths, format="wav", channels=2))

    def answer_text_to_audio(self, text):
        sample_rate = 48000
        if text == "":
            return

        speaker = ''
        text_input = ''

        if self.lang == 'rus':
            speaker = 'eugene'
            text_input = text

        if self.lang == 'eng':
            speaker = 'en_20'
            text_input = self.translator.translate(text=text, dest='en').text

        audio_paths = self.model.save_wav(text=text_input,
                                          speaker=speaker,
                                          sample_rate=sample_rate)
        p = multiprocessing.Process(target=self.run_audio(audio_paths))
        p.start()
