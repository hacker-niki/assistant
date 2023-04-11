# предлагаю эту часть кода сделать, как у максима, но поищу еще варианты
import json
from assistant import Assistant


class Translation:
    # Получение вшитого в приложение перевода строк для создания мультиязычного ассистента
    # with open("translations.json", "r", encoding="UTF-8") as file:
    #     translations = json.load(file)

    def __init__(self):
        pass

    def get(self, text: str, speech_language):
        #
        # Получение перевода строки из файла на нужный язык (по его коду)
        # :param text: текст, который требуется перевести
        # :return: вшитый в приложение перевод текста
        #
        if text in self.translations:
            return self.translations[text][speech_language]
        else:
            # в случае отсутствия перевода происходит вывод сообщения об этом в логах и возврат исходного текста
            print("Not translated phrase: {}".format(text))
            return text
