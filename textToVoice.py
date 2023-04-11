# assistant
import pyttsx3

class TextToVoice:
    def __init__(self):
        self.engine = pyttsx3.init()

    def text_to_voice(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
