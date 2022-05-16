import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import ACTION, ACCOUNT_NAME,USER, RESPONSE, PRESENCE, TIME, ERROR
from server import process_client_message

class TestServer(unittest.TestCase):
    # в сервере только 1 функция для тестирования
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    ok_dict = {RESPONSE: 200}

    def test_ok_check(self):
#         корректныйзапрос
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 20.20, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

    def test_no_action(self):
        # Ошибка если нет действия
        self.assertEqual(process_client_message (
            {TIME: 20.20, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
    #     Oшибка если неизвестное действие
        self.assertEqual(process_client_message(
            {ACTION: 'Wrong', TIME: 20.20, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)


    def test_no_time(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)




    def test_no_user(self):
        # ошибка нет пользователя
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 20.20}), self.err_dict)


    def test_unknown_user(self):
        # щшибка нет Guest
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 20.20, USER: {ACCOUNT_NAME: 'Guest2'}}), self.err_dict)


if __name__ == '__main__':
    unittest.main()