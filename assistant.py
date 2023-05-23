import json
from sys import exit

import pvporcupine
from pvrecorder import PvRecorder

import audioProcessor
import textHandler


class Assistant:
    def __init__(self):
        # Создаем объект для синтеза речи
        try:
            self.handler = textHandler.TextHandler()
            self.audio = audioProcessor.AudioProcessor()
            self.audio.answer_text_to_audio("Здарова, Меченый!")
        except:
            print("Ошибка инициализации")

    def run(self):
        with open('data.json', 'r') as file:
            data = json.load(file)
            key = data['picovoice_key']
        access_key = key  # надо сделать интерфейс вставки своего ключа
        keyword_paths = ['data\\model_hey_quant.ppn']
        handle = None
        recorder = None
        try:
            handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths, sensitivities=[0.7])
            recorder = PvRecorder(device_index=-1, frame_length=512)
        except:
            self.audio.answer_text_to_audio("Не удалось запустить модуль ответа, проверьте ключи доступа!")
            return

        while True:
            pcm = None
            keyword_index = None
            try:
                recorder.start()
                pcm = recorder.read()
                keyword_index = handle.process(pcm)
            except:
                self.audio.answer_text_to_audio("Происходит ошибка распознавания, поробуйте позже!")
                return
            if keyword_index >= 0:
                recorder.stop()
                while True:
                    command = self.recognize_speech()
                    answer = self.handler.map_string_to_function(command)
                    if not answer[0]:
                        self.audio.answer_text_to_audio("Завершаю работу")
                        exit(0)
                    try:
                        self.audio.answer_text_to_audio(answer[1])
                        break
                    except:
                        self.audio.answer_text_to_audio("Ошибка во время выполнения функции!")
                        break


# Функция для распознавания речи
    def recognize_speech(self):
        # os.remove("microphone-results.wav")
        self.audio.answer_text_to_audio("Да, господин")
        return self.audio.record_and_recognize_audio()

    # Функция для выполнения команд
    def process_command(self, command) -> bool:
        result = self.handler.map_string_to_function(input_string=command)
        self.audio.answer_text_to_audio(result[1])
        return result[0]
