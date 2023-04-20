import unittest

from awesom_o import (
    BET_RANGE, CARTMAN, CREATOR, INNA, KENNY, KEP4IK, LEMUR, MARIK, MARINA,
    MARKLAR, CITY_NAME, ZAJA, ZERO
)


class TestRegularExpression(unittest.TestCase):
    """Проверка используемых регулярных выражений."""
    def test_dices(self):
        message = 'Неверное выражение для ставок в кости!'
        right_dices = ('3 11', '5 7', '4 9')
        wrong_dices = ('2 12', '1 15', '6')
        for dice in right_dices:
            with self.subTest(value=dice):
                self.assertRegex(dice, BET_RANGE, msg=message)
        for dice in wrong_dices:
            with self.subTest(value=dice):
                self.assertNotRegex(dice, BET_RANGE, msg=message)

    def test_hidden_phrases(self):
        message = 'Неверное выражение для пасхалок!'
        cases = [
            ('Слышал про Эрика Картмана?', CARTMAN),
            ('Эрик Картманн крутой чувак!', CARTMAN),
            ('Они убили Кени!', KENNY),
            ('они убили Кенни!', KENNY),
            ('Видел серию про Марклар.', MARKLAR),
            ('На маркларе сейчас лето...', MARKLAR),
            ('Умеешь притворяться ноликом?', ZERO),
            ('Давай, притворись ноликом', ZERO)
        ]
        for phrase, regex in cases:
            with self.subTest(phrase=phrase):
                self.assertRegex(phrase, regex, msg=message)

    def test_dossiers(self):
        message = 'Неверное выражение для секретных досье!'
        cases = [
            ('Кто такой Создатель?', CREATOR),
            ('Кто такая Мыша?', INNA),
            ('Кто такой Кэп?', KEP4IK),
            ('Кто такая Лемур?', LEMUR),
            ('Кто такой Марик?', MARIK),
            ('Кто такая Маришка?', MARINA),
            ('Кто такой Зажа?', ZAJA)
        ]
        for phrase, regex in cases:
            with self.subTest(phrase=phrase):
                self.assertRegex(phrase, regex, msg=message)

    def test_city_name(self):
        message = 'Неверное выражение для названия города!'
        right_cities = [
            'Петропавловск-Камчатский', 'Комсомольск-на-Амуре', 'Москва',
            'Нижний Новгород'
        ]
        wrong_cities = [
            'Город из четырёх слов', '&Пятигорск', '5Орёл', 'fКазань',
            'Ростоv', 'Ми$лан', 'Оченьуждлинноеназваниевымышленногогорода'
        ]
        for city in right_cities:
            with self.subTest(city=city):
                self.assertRegex(city, CITY_NAME, msg=message)
        for city in wrong_cities:
            with self.subTest(value=city):
                self.assertNotRegex(city, CITY_NAME, msg=message)


if __name__ == '__main__':
    unittest.main()

# подробный запуск python -m unittest -v tests.py
