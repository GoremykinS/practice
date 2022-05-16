import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import ACTION, ACCOUNT_NAME,USER, RESPONSE, PRESENCE, TIME, ERROR
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    # класс в тестами

    def test_def_presense(self):
        # тест корректного запроса
        test = create_presence()
        #     время необходимо приравнять принудительно иначе тест не будет пройден
        test[TIME] = 20.20
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 20.21, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        # Тест корректного разбора ответа 200
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_400_ans(self):
        # Тест корректного разбора 400
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')



if __name__ == '__main__':
    unittest.main()