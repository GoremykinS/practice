import os
import sys
import datetime
import logging.handlers
import time

sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import LOGGING_LEVEL, ENCODING



# создаем формировщик логов (formatter):
SERVER_FORMATTER = logging.Formatter('%(asctime)s%(levelname) 8s %(filename)s %(message)s')
NOW_DATETIME = (datetime.datetime.now()).strftime('%d-%m-%Y %H:%M')

# подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, f'server.log {NOW_DATETIME}')

# создаем потоки вывода логов

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE =logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

# создаем регистратор

LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)


# отладка

if __name__ == '__main__':
    LOGGER.critical('критическая ошибка')
    LOGGER.error('ошибка')
    LOGGER.debug('отладочная информация')
    LOGGER.info('информационное сообще')




