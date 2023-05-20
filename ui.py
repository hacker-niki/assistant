import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox, QComboBox
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
import json
import sounddevice as sd
import tkinter as tk
from assistant import Assistant
import app
import user
from user import client
#jhjh
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkPDFViewer import tkPDFViewer as pdf
import FirstWindow

amount = 0
class PushButton_start(QPushButton):
    def __init__(self, parent=None):
        super(PushButton_start, self).__init__(parent)
        self.setIcon(QIcon('uiData/start_light.png'))
        self.setIconSize(QSize(100, 100))

    def mousePressEvent(self, event):
        self.setIcon(QIcon('uiData/start_dark.png'))
        self.setIconSize(QSize(100, 100))
        self.start_button_pressed()

    def mouseReleaseEvent(self, event):
        self.setIcon(QIcon('uiData/start_light.png'))
        self.setIconSize(QSize(100, 100))
        assistant = Assistant()
        assistant.run()

    def start_button_pressed(self):
        if os.stat('data.json').st_size != 0:
            with open("data.json", "r") as f:
                data = json.load(f)
                username = data['username']
                town = data['town']
                picovoice_key = data['picovoice_key']
                openAI_key = data['openAI_key']
                language = data['language']
                if (username == '') | (town == '') | (picovoice_key == '') | (openAI_key == ''):
                    self.open_new_window()
                print(data)
        else:
            self.open_new_window()

    def open_new_window(self):
        global amount
        amount += 1
        if (amount == 1):
            window = FirstWindow.App()
            FirstWindow.auto_fill()
            FirstWindow.App.window.mainloop()
        else:
            show_message()
    #def open_new_window(self):
     #   self.new_window = NewWindow()
      #  self.new_window.show()

class PushButton_log_in(QPushButton):
    def __init__(self, parent=None):
        super(PushButton_log_in, self).__init__(parent)
        self.setIcon(QIcon('uiData/log_in_light.png'))
        self.setIconSize(QSize(100, 100))

    def mousePressEvent(self, event):
        self.setIcon(QIcon('uiData/log_in_dark.png'))
        self.setIconSize(QSize(100, 100))

        self.open_new_window()

    def mouseReleaseEvent(self, event):
        self.setIcon(QIcon('uiData/log_in_light.png'))
        self.setIconSize(QSize(100, 100))

    def open_new_window(self):
        global amount
        amount += 1
        if (amount==1):
            window = FirstWindow.App()
            FirstWindow.auto_fill()
            print(1)
            FirstWindow.App.window.mainloop()
        else:
            show_message()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('uiData/form1.ui', self)
        self.setWindowTitle("Jarvis")
        self.setStyleSheet("background-color: #000000;")
        self.path_to_silent_video = 'uiData/silent_video.avi'
        self.path_to_speech_video = 'uiData/speaking_video.avi'
        # Ширина и высота видео-заставки.

        self.width_video = 470
        self.height_video = 350
        self.setFixedSize(self.width_video, self.height_video)

        self.pushButton = PushButton_log_in(self)
        self.pushButton.move(20, 20)

        self.pushButton2 = PushButton_start(self)
        self.pushButton2.move(190, 300)

        self.label = QLabel(self)
        self.label.move(330, 270)
        self.label.setFixedWidth(150)
        self.label.setStyleSheet("background: black;")

        # Определение вариантов ответов
        self.variant_options = [' rus', ' eng']

        # Создание элементов окна
        self.buttonCombo = QComboBox(self)
        self.buttonCombo.move(130, 20)
        self.buttonCombo.setFixedSize(65, 31)
        self.buttonCombo.addItems(self.variant_options)
        self.buttonCombo.currentIndexChanged.connect(self.onClick)

        # Установка стиля
        self.buttonCombo.setStyleSheet('QComboBox::drop-down {border: none;} \
                                                 QComboBox::down-arrow \
                                                 {image: url(down_arrow.png);} \
                                                 QComboBox {border-radius: 15px; \
                                                 padding: 1px 18px 1px 3px; \
                                                 background-color: #9d3abf;\
                                                 color: white; \
                                                 font-size: 15px;}')

        self.is_assistant_talking = 0
        # Запускаем заставку.
        self.media1 = QtMultimedia.QMediaPlayer(self)
        self.media1.setVideoOutput(self.video)
        self.media1.setMedia(
            QtMultimedia.QMediaContent(
                QtCore.QUrl.fromLocalFile(self.path_to_silent_video)
            )
        )
        self.media1.play()
        # Отслеживаем статус видео, чтобы скрыть его после проигрывания.
        self.media1.mediaStatusChanged.connect(self.start_new_video)

    # Функция, запускающая видео
    def start_new_video(self, status):
        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            if self.is_assistant_talking == 1:
                self.media1.setMedia(
                    QtMultimedia.QMediaContent(
                        QtCore.QUrl.fromLocalFile(self.path_to_speech_video)
                    )
                )
            else:
                self.media1.setMedia(
                    QtMultimedia.QMediaContent(
                        QtCore.QUrl.fromLocalFile(self.path_to_silent_video)
                    )
                )
            self.media1.play()

    def setIsAssistantTalking(self, status):
        self.is_assistant_talking = status

    def onClick(self):
        # Обработка выбора варианта ответа
        selected_variant = self.variant_options[self.buttonCombo.currentIndex()]

        with open('data.json', 'r') as file:
            data = json.load(file)

        # Изменяем значение ключа "example_key"
        data["language"] = selected_variant

        # Открываем файл на запись и сохраняем изменения
        with open('data.json', 'w') as file:
            json.dump(data, file)

        print(f'Выбран вариант: {selected_variant}')



def show_message():
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Предупреждение")
    msg_box.setText("Вы уже успели зарегестрироваться! Перезапустите приложение или нажмите \"Start\"")

    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setStyleSheet("background-color: #4C5B79; color: white;")
    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg_box.setDefaultButton(QMessageBox.Cancel)

    response = msg_box.exec_()

    if response == QMessageBox.Ok:
        print("Нажата кнопка ОК")
    else:
        print("Нажата другая кнопка")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.move(100, 100)
    ex.show()
    sys.exit(app.exec_())