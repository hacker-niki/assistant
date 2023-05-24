import json
import multiprocessing
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox, QComboBox, QHBoxLayout
from PyQt5 import QtCore, QtMultimedia
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox
from PyQt5.QtWidgets import QComboBox

import FirstWindow
from app import startAssistant

amount = 0

class Manual(QWidget):
    def __init__(self,
                 parent=None):  # если собрался передавать аргументы, то не забудь их принять (nameofargument, self, parent=None)
        super().__init__(parent, QtCore.Qt.Window)
        self.build()  # ну и передать в открывающееся окно соответственно (nameofargument, self)

    def build(self):
        self.setGeometry(300, 300, 300, 300)
        hbox = QHBoxLayout(self)
        pixmap = QPixmap("uiData/Квант.png")
        pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(20, 20)
        self.setWindowTitle('Red Rock')
        self.setWindowTitle('MANUAL')
##

class MainWindow(QMainWindow):
    tray_icon = None
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('uiData/form1.ui', self)
        self.setWindowTitle("Quant")
        self.setStyleSheet("background-color: #7e7e7e;")
        self.path_to_silent_video = 'uiData/video.avi'
        self.path_to_speech_video = 'uiData/video.avi'

        self.width_video = 470
        self.height_video = 350
        self.setFixedSize(self.width_video, self.height_video)

        #self.pushButton_start = PushButton_log_in(self)
        #self.pushButton_start.move(20, 20)

        #self.pushButton2 = PushButton_start(self)
        #self.pushButton2.move(190, 300)

        # Определение вариантов ответов
        self.variant_options = ['rus', 'eng']

        self.pushButton_log_in = QPushButton("LOG IN", self)
        self.pushButton_log_in.move(20, 20)
        self.pushButton_log_in.clicked.connect(self.open_new_window)

        # Установка стиля
        self.pushButton_log_in.setStyleSheet('QPushButton::drop-down {border: none;} \
                                                                         QPushButton::down-arrow \
                                                                         {image: url(down_arrow.png);} \
                                                                         QPushButton {border-radius: 15px; \
                                                                         background-color: #9d3abf;\
                                                                         color: white; \
                                                                         font-family: Arial;\
                                                                         font-weight: 1px;\
                                                                         font-size: 15px;}')

        self.pushButton_start = QPushButton("START", self)
        self.pushButton_start.move(350, 300)
        self.pushButton_start.clicked.connect(self.start_button_pressed)

        # Установка стиля
        self.pushButton_start.setStyleSheet('QPushButton::drop-down {border: none;} \
                                                                 QPushButton::down-arrow \
                                                                 {image: url(down_arrow.png);} \
                                                                 QPushButton {border-radius: 15px; \
                                                                 background-color: #9d3abf;\
                                                                 color: white; \
                                                                 font-family: Arial;\
                                                                 font-weight: 1px;\
                                                                 font-size: 15px;}')


        # Создание элементов окна
        self.buttonCombo = QComboBox(self)
        self.buttonCombo.move(387, 60)
        self.buttonCombo.setFixedSize(65, 31)
        self.buttonCombo.addItems(self.variant_options)
        self.buttonCombo.currentIndexChanged.connect(self.onClick)

        # Установка стиля
        self.buttonCombo.setStyleSheet('QComboBox::drop-down {width: 20px;} \
        QComboBox::down-arrow {image: url(down_arrow.png); width: 10px;}\
                                                 QComboBox {border-radius: 15px; \
                                                 padding: 1px 10px 1px 15px; \
                                                 background-color: #9d3abf;\
                                                 color: white; \
                                                 font-size: 15px;}')

        self.buttonManual = QPushButton('MANUAL', self)
        self.buttonManual.resize(85, 31)
        self.buttonManual.move(370, 20)
        self.buttonManual.clicked.connect(self.openMan)

        # Установка стиля
        self.buttonManual.setStyleSheet('QPushButton::drop-down {border: none;} \
                                                         QPushButton::down-arrow \
                                                         {image: url(down_arrow.png);} \
                                                         QPushButton {border-radius: 15px; \
                                                         background-color: #9d3abf;\
                                                         font-family: Arial;\
                                                         color: white; \
                                                         font-size: 13px;}')

        self.is_assistant_talking = 0
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

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('uiData/icon.png'))
        start_action = QAction("MANUAL", self)
        start_action.triggered.connect(self.openMan)
        tray_menu = QMenu()
        tray_menu.addAction(start_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

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

    def openMan(self):
        self.manual = Manual(self)  # здесь можешь передавать аргументы во второе окно (nameofargument, self)
        self.manual.show()

    def hideMainWindow(self):
        self.hide()

    def start_button_pressed(self):
        if os.stat('data.json').st_size != 0:
            with open("data.json", "r") as f:
                data = json.load(f)
                username = data['username']
                town = data['town']
                picovoice_key = data['picovoice_key']

                language = data['language']
                if (username == '') | (town == '') | (picovoice_key == ''):
                    self.open_new_window()
                print(data)

                self.hide()
                t = multiprocessing.Process(target=startAssistant())
                t.start()
                t.join()

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
