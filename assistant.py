import pyttsx3
import speech_recognition as sr
import textHandler
import TextToVoice


class Assistant:
    def __init__(self):
        # Создаем объект для синтеза речи
        
        self.speak = TextToVoice.TextToVoice()
        self.handler = textHandler.TextHandler()

        self.speak.text_to_voice("Здарова, Меченый!")

    def run(self):
        while True:
            command = self.recognize_speech()
            if not self.process_command(command):
                break
                
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
    def process_command(self, command) -> bool:
        result = self.handler.map_string_to_function(input_string=command)
        self.speak.text_to_voice(result[1])
        return result[0]
