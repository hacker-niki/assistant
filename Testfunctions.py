import datetime
import unittest

from functions import coin_function
from functions import commands_function
from functions import default_function
from functions import doing_function
from functions import hello_function
from functions import joke_function
from functions import mood_function
from functions import random_function
from functions import stop_function
from functions import time_function


class MyTestCase(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(hello_function(""), "Хабар принес?")

    def test_doing(self):
        self.assertEqual(doing_function(""), "Можно и передохнуть маленько")

    def test_stop(self):
        self.assertEqual(stop_function(""), "Ну, удачной охоты, сталкер.")

    def test_time(self):
        now = datetime.datetime.now()
        self.assertEqual(time_function(""), "Сейчас " + str(now.hour) + ":" + str(now.minute))

    def test_default(self):
        self.assertEqual(default_function(""), "Не удалось распознать команду.")

    def test_mood(self):
        self.assertEqual(mood_function(""), "Какие дела могут быть у робота? Не крашнулся и то хорошо")

    def test_commands(self):
        self.assertEqual(commands_function(""),
                         "Пока что я могу: повторить за вами, настроить яркость и звук, выключить компьютер, изменить расскладку клавиатуры, подбросить монетку, рассказать или написать что-нибудь, найти информацию в интернете, рассказать прогноз погоды, найти видео в ютубе, рассказать анекдот, сказать сколько сейчас времени, найти определение в википедии, настроить данные о пользователе,  поприветсвовать вас, попрощаться с вами, найти песню в спотифай, также вы можете поинтересоваться как у меня дела")

    # def test_translator(self):
    #  self.assertEqual(translator_function("Good day"), "Хороший день")

    def test_random(self):
        self.assertTrue(1 <= random_function("от 1 до 100") <= 100)

    def test_coin(self):
        sentences = ["Выпал орел", "Выпала решка"]
        self.assertIn(coin_function(""), sentences)

    def test_joke(self):
        sentences = ["Если вы внезапно оказались в яме, первое, что нужно сделать - перестать копать!",
                     "Штирлиц уходил от ответа, ответ неотступно следовал за ним.",
                     "Уходя из квартиры, делай селфи с утюгом! Так ты избежишь ненужных сомнений.",
                     "Колобок повесился, ахаххаха"]
        self.assertIn(joke_function(""), sentences)


if __name__ == '__main__':
    unittest.main()
