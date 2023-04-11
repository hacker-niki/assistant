import pyttsx3
import speech_recognition as sr
import textHandler
import audioProcessor


class Assistant:
    def __init__(self):
        # Создаем объект для синтеза речи
        self.handler = textHandler.TextHandler()
        self.audio = audioProcessor.AudioProcessor()
        self.audio.answer_text_to_audio("Здарова, Меченый!")
<<<<<<< HEAD
        self.handler = textHandler.TextHandler()
=======
>>>>>>> 4f883dea4867365920cf61f2d1053ec5f962d0ff

    def run(self):
        while True:
            command = self.recognize_speech()
            answer = self.handler.map_string_to_function(command)
            if not answer[0]:
                break
<<<<<<< HEAD
            self.audio.answer_text_to_audio(answer[1])
=======
>>>>>>> 4f883dea4867365920cf61f2d1053ec5f962d0ff

    # Функция для распознавания речи

    def recognize_speech(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Говорите...")
            audio = r.listen(source, phrase_time_limit=5)
            return self.audio.audio_to_text(audio=audio)

    # Функция для выполнения команд
    def process_command(self, command) -> bool:
        result = self.handler.map_string_to_function(input_string=command)
        self.audio.answer_text_to_audio(result[1])
        return result[0]
