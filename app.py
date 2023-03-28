import pyttsx3
import speech_recognition as sr
import datetime

# Создаем объект для синтеза речи
engine = pyttsx3.init()

# Устанавливаем голос для синтеза речи
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Функция для воспроизведения речи
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для распознавания речи
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ru-RU')
            print("Вы сказали: {}".format(text))
            return text
        except:
            print("Не удалось распознать речь")
            return ""

# Функция для выполнения команд
def process_command(command):
    if "привет" in command.lower():
        speak("Привет! Как дела?")
    elif "как дела" in command.lower():
        speak("У меня все хорошо, спасибо. А у тебя?")
    elif "который час" in command.lower():
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif "стоп" in command.lower():
        speak("До свидания!")
        return True
    return False

# Главный цикл программы
while True:
    command = recognize_speech()
    if process_command(command):
        break
