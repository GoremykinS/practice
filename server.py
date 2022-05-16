# сервер

import sys
import json
import socket
import time

import argparse
import logging


from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


SERVER_LOGGER = logging.getLogger('server')


def process_client_message(message):
    # обработка сообщений от клиента, принимает словарь - сообщение от клиента,
    # проверяет корректность, возвращает словарь ответ для клиента



    SERVER_LOGGER.debug(f'разраб сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return{
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def create_arg_parser():
    # парсер аргументов коммандной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('a', default='', nargs='?')
    return  parser




def main():
    # проверка параметров командной строки, если нет параметров, то задаем значение по умолчанию.


    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверим подходящий номер порта
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(
            f'попытка запуска сервера с указанием неподходящего порта: {listen_port}.'
            f'допустимы адреса с 1024 до 65535. ')
        sys.exit(1)

    SERVER_LOGGER.info(f'Запущен сервер, порт для подключения: {listen_port},'
                       f'фдрес с котороо принимается подключения: {listen_address},'
                       f'есди адрес не указан, принимаютсясоединения с любых адресов.')

    # готовый сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # слушаем порт

    transport.listen(MAX_CONNECTIONS)


    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'установленно соединение с ПК {client_address}' )
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'полученно сообщение {message_from_client}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'сформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'соединение с клиентом {client_address} закрывается')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'не удалось декодировать Json строку полученную от'
                f'клиента {client_address}, Соединение закрывается')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'от клиента {client_address} приняты некоректные данные.'
                                f'соединение закрывается')
            client.close()

if __name__ == '__main__':
    main()


