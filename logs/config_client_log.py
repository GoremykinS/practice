import os
import sys
import json
import socket
import time

import argparse
import logging


sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import LOGGING_LEVEL, ENCODING


# создаем формировщик логов (formatter):
CLIENT_FORMATTER = logging.Formatter('%(asctime)s%(levelname) 8s %(filename)s %(message)s')

# подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# создаем потоки вывода логов

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE =logging.FileHandler(PATH, encoding=ENCODING)
LOG_FILE.setFormatter(CLIENT_FORMATTER)

# создаем регистратор

LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)


# отладка

if __name__ == '__main__':
    LOGGER.critical('критическая ошибка')
    LOGGER.error('ошибка')
    LOGGER.debug('отладочная информация')
    LOGGER.info('информационное сообщение')