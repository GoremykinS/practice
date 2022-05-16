import sys
import json
import socket
import time

import argparse
import logging
import logs.config_client_log
from errors import ReqFieldMissingError


from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT

from common.utils import get_message, send_message

# инициация клиетновского логера
CLIENT_LOGGER = logging.getLogger('client')


def create_presence(account_name='Guest'):
    #     функция генерирует запрос о присутвии клиента

    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    CLIENT_LOGGER.debug(f'сформированно {PRESENCE} сообщение для пользователя {account_name}')
    return out


def process_ans(message):
    # функция разбирает ответ сервера

    CLIENT_LOGGER.debug(f'разбор сообщения от сервера: {message}')

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


def create_arg_parser():
    # создаем парсер аргументов коммандной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return  parser





def main():
    # загружаем параметры командной строки
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'попытка запускаклиента с неподходящим номром порта: {server_port}.'
            f'допустимы адреса с 1024 до 65535. Клиент завершаетсяю ')
        sys.exit(1)

    CLIENT_LOGGER.info(
        f'запущен клиент с параметрами: '
        f'адресс сервера: {server_address}, порт: {server_port}'
    )

    #   иницализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_ans(get_message(transport))
        transport.close()
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('не удалосьдекодировать полученную json строку.')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'не удалось подключиться ксерверу {server_address}:{server_port},'
                               f'конечный компьютеротверг запрос на подключение.')


    except ReqFieldMissingError as messing_error:
        CLIENT_LOGGER.error(f'в ответе сервера отсутвует необходимое поле'
                            f'{missing_error.missing_field}')


if __name__ == '__main__':
    main()
