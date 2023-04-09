import SpeechRecognition as sr
import pyttsx3
class AudioProcessor():
    def audio_to_text(audio):
        #функция перевода текстa в аудио
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio, language = "ru-Ru").lower()
            return text
        except sr.RequestError:
            print("Что-то с интернетом(( Проверьте подключение, пожалуйста")
        except sr.UnknownValueError:
            print("Не расслышал, что Вы сказали. Повторите")

    def answertext_to_audio(text):
        #функция воспроизведения текста
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

