import pyttsx3
import speech_recognition as sr
import textHandler
import audioProcessor
import user
import pvporcupine
from pvrecorder import PvRecorder


class Assistant:
    def __init__(self):
        # Создаем объект для синтеза речи
        self.handler = textHandler.TextHandler()
        self.audio = audioProcessor.AudioProcessor()
        self.audio.answer_text_to_audio("Здарова, Меченый!")
        self.handler = textHandler.TextHandler()

    def run(self):
        access_key = ''  # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
        keyword_paths = ['C:/Users/Lenovo/Downloads/Telegram Desktop/model']
        handle = pvporcupine.create(access_key="r10k7RyJ6Dc5R9PE0PuA0saOtZmbF70H6ej5JH/nwSiTzQkx9BCAZg==",
                                    keyword_paths=keyword_paths, sensitivities=[1])
        recorder = PvRecorder(device_index=1, frame_length=512)

        while True:
            recorder.start()
            pcm = recorder.read()
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                recorder.stop()
                while True:
                    command = self.recognize_speech()
                    answer = self.handler.map_string_to_function(command)
                    if not answer[0]:
                        self.audio.answer_text_to_audio("Не удалось распознать команду")
                        break
                    self.audio.answer_text_to_audio(answer[1])
                    break

    # Функция для распознавания речи

    def recognize_speech(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.audio.answer_text_to_audio("Да, господин, слушаю команду")
            audio = r.listen(source, phrase_time_limit=5)
            return self.audio.audio_to_text(audio=audio)

    # Функция для выполнения команд
    def process_command(self, command) -> bool:
        result = self.handler.map_string_to_function(input_string=command)
        self.audio.answer_text_to_audio(result[1])
        return result[0]
