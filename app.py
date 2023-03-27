import speech_recognition as sr
import pyttsx3

# создаем объект для распознавания речи
r = sr.Recognizer()

# создаем объект для синтеза речи
engine = pyttsx3.init()
engine.say("I will speak this text")

# задаем голос для синтеза речи
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # выбираем женский голос


# функция для синтеза речи
def speak(t):
    engine.say(t)
    engine.runAndWait()


# функция для распознавания речи
def recognize_speech():
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="ru-RU")
            print("Вы сказали: " + text)
            return text
        except sr.UnknownValueError:
            print("Речь не распознана")
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания речи; {0}".format(e))


# основной код для голосового ассистента
if __name__ == '__main__':
    # получаем речь от пользователя
    text = recognize_speech()

    # обрабатываем команду и генерируем ответ
    if "привет" in text:
        speak("Здравствуйте, чем я могу вам помочь?")
    elif "как дела" in text:
        speak("У меня всё хорошо, спасибо за ваш интерес!")
    else:
        speak("Извините, я не поняла вашей команды.")
