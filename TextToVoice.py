# assistant
import pyttsx3

def text_to_speech(text, voice='english', rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
