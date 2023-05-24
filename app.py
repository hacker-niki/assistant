import multiprocessing

from assistant import Assistant


def startAssistant():
    # try:
    assistant = Assistant()
    assistant.run()
    # except:
    #     print("Неизвестная ошибка ассистента")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    startAssistant()
