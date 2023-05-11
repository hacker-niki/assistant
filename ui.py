import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
import json
import sounddevice as sd
from assistant import Assistant
import app
import user
from user import client

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('uiData/form1.ui', self)
        self.setWindowTitle("Jarvis")
        self.setStyleSheet("background-color: #1b1034;")

        self.path_to_silent_video = 'uiData/stop_Animation.avi'
        self.path_to_speech_video = 'uiData/anim.avi'
        # Ширина и высота видео-заставки.

        self.width_video = 470
        self.height_video = 350
        self.setFixedSize(self.width_video, self.height_video)

        self.pixmap_log_in = QPixmap("uiData/log-in.png")

        self.pushButton = QPushButton(self)
        self.pushButton.setIcon(QIcon(self.pixmap_log_in))
        self.pushButton.setIconSize(QSize(100, 100))
        #self.pushButton.setIconSize(self.pixmap_log_in.size())
        self.pushButton.move(20, 20)
        self.pushButton.clicked.connect(self.open_new_window)
        #self.pushButton.setStyleSheet("background-color: #5a6885;")

        self.pixmap_start = QPixmap("uiData/start.png")

        self.pushButton2 = QPushButton(self)
        self.pushButton2.setIcon(QIcon(self.pixmap_start))
        self.pushButton2.setIconSize(QSize(100, 100))
        self.pushButton2.move(190, 300)
        self.pushButton2.clicked.connect(self.start_button_pressed)

        self.is_assistant_talking = 1
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

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()

    def start_button_pressed(self):
        if os.stat('../../../Downloads/Telegram Desktop/data.json').st_size != 0:
            with open("../../../Downloads/Telegram Desktop/data.json", "r") as f:
                data = json.load(f)
                key = data['key']
                #client.town = data['town']
                town = data['town']
                language = data['language']
                if (key=='') | (town =='') | (language ==''):
                    self.open_new_window()
                assistant = Assistant()
                assistant.run()
                print(data)
        else:
            self.open_new_window()


class NewWindow(QMainWindow):
    def __init__(self):
        super(NewWindow, self).__init__()
        self.setWindowTitle('Log in')
        self.setStyleSheet("background-color: #4C5B79;")
        self.setFixedSize(300, 350)

        self.pixmap1 = QPixmap("uiData/key_porcupine_.png")
        self.pixmap1_resized = self.pixmap1.scaled(118, 13)
        self.label1 = QLabel(self)
        self.label1.setPixmap(self.pixmap1_resized)
        self.label1.setFixedSize(self.pixmap1_resized.size())
        #self.label1 = QLabel('Key porcupine:', self)
        self.label1.move(20, 25)
        #self.label1.setStyleSheet("color: white;")
        self.line1 = QLineEdit(self)
        self.line1.setFixedWidth(150)
        self.line1.move(20, 50)

        self.pixmap2 = QPixmap("uiData/town_.png")
        self.pixmap2_resized = self.pixmap2.scaled(45, 13)
        self.label2 = QLabel(self)
        self.label2.setPixmap(self.pixmap2_resized)
        self.label2.setFixedSize(self.pixmap2_resized.size())
        self.label2.move(20, 90)
        #self.label2.setStyleSheet("color: white;")
        self.line2 = QLineEdit(self)
        self.line2.setFixedWidth(150)
        self.line2.move(20, 110)

        self.pixmap3 = QPixmap("uiData/language_.png")
        self.pixmap3_resized = self.pixmap3.scaled(81, 13)
        self.label3 = QLabel(self)
        self.label3.setPixmap(self.pixmap3_resized)
        self.label3.setFixedSize(self.pixmap3_resized.size())
        self.label3.move(20, 150)
        #self.label3.setStyleSheet("color: white;")
        self.line3 = QLineEdit(self)
        self.line3.setFixedWidth(150)
        self.line3.move(20, 170)

        self.pixmap_micro = QPixmap("uiData/autofill.png")

        self.pushButton1 = QPushButton(self)
        self.pushButton1.setStyleSheet("background-color: #831571")
        self.pushButton1.setIcon(QIcon(self.pixmap_micro))
        self.pushButton1.setIconSize(QSize(70, 20))
        self.pushButton1.setGeometry(20, 210, 70, 20)
        self.pushButton1.clicked.connect(self.autofill_data)

        self.pixmap_micro = QPixmap("uiData/micro.png")

        self.pushButton2 = QPushButton(self)
        self.pushButton2.setStyleSheet("background-color: #831571")
        self.pushButton2.setIcon(QIcon(self.pixmap_micro))
        self.pushButton2.setIconSize(QSize(20, 20))
        self.pushButton2.move(20, 260)
        self.pushButton2.setGeometry(20, 280, 30, 30)
        self.pushButton2.clicked.connect(self.check_microphone)

        self.label = QLabel(self)
        self.label.setGeometry(20, 230, 200, 20)

        self.pixmap_start = QPixmap("uiData/accept.png")

        self.pushButton3 = QPushButton(self)
        self.pushButton3.setIcon(QIcon(self.pixmap_start))
        self.pushButton3.setIconSize(QSize(100, 100))
        #self.button2.setGeometry(180, 260, 100, 20)
        self.pushButton3.move(180, 280)
        self.pushButton3.clicked.connect(self.get_text)

    def get_text(self):
        key = self.line1.text()
        town = self.line2.text()
        language = self.line3.text()

        data = {
            "key": key,
            "town": town,
            "language": language
        }

        with open("../../../Downloads/Telegram Desktop/data.json", "w") as f:
            json.dump(data, f)

        print(key)
        self.close()

    def check_microphone(self):
        try:
            sd.query_devices()
            self.label.setText("Microphone is working!")
        except OSError:
            self.label.setText("Microphone is not available")

    def autofill_data(self):
        with open('../../../Downloads/Telegram Desktop/data.json', 'r') as f:
            data = json.load(f)
        key = data['key']
        town = data['town']
        language = data['language']
        self.line1.setText(key)
        self.line2.setText(town)
        self.line3.setText(language)
        print('Data autofilled')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
