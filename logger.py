import logging
import os
from logging.handlers import TimedRotatingFileHandler
from environs import Env
from time import time


env = Env()
env.read_env()

APP_LOG_DIR = env.str("APP_LOG_DIR", default='Logs')  # Папка логов
READOUT_INTERVAL = env.str("READOUT_INTERVAL", default=10)  # интервал записи показаний


class FacilityLogger (object):
    def __init__(self, facility):
        self.id = id
        self.logger = logging.getLogger(f'faciliti {facility.id}')
        if not os.path.isdir(f"{APP_LOG_DIR}/{facility.id}"):
            os.mkdir(f"{APP_LOG_DIR}/{facility.id}")
        self.logger_handler = TimedRotatingFileHandler(f'{APP_LOG_DIR}/{facility.id}/{facility.id}.log',
                                                       encoding='utf-8',
                                                       when='midnight',
                                                       backupCount=30)
        self.logger.addHandler(self.logger_handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.info(f'\nМониторинг объекта "{facility.name}"  (ID: {facility.id})')
        self.logger.info(f'    Адрес: {facility.addr}')
        self.logger.info(f'    Линии:')
        for sens in facility.sensors:
            self.logger.info(f'        {sens.addr}/{sens.input} - {sens.name}')
        self.logger.info('-' * (31 + 10 * len(facility.sensors)))
        s = '|  Время'.ljust(29) + '|'
        for sens in facility.sensors:
            s = s + f' {sens.addr}/{sens.input}'.ljust(10) + '|'
        self.logger.info(s)
        self.logger.info('-' * (31 + 10 * len(facility.sensors)))

        self.logger_handler.setFormatter(logging.Formatter('|  %(asctime)s   |' + '%(message)s'))
        self.last_readoud = 0

    def readout(self, facility):
        now = time()
        if now - self.last_readoud < READOUT_INTERVAL:
            return
        s = ''
        for sens in facility.sensors:
            s = s + f' {sens.readout}'.ljust(10) + '|'
        self.logger.info(s)
        self.last_readoud = now


def del_logger(id):
    if id in fclt_logger.keys():
        fclt_logger[id].logger.handlers.clear()
        fclt_logger[id].logger.propagate = False
        fclt_logger.pop(id)


app_logger = logging.getLogger('tsub')
if not os.path.isdir(APP_LOG_DIR):
    os.mkdir(APP_LOG_DIR)
app_logger_handler = TimedRotatingFileHandler(f'{APP_LOG_DIR}/tsub_srv.log',
                                              encoding='utf-8',
                                              when='midnight',
                                              backupCount=30)
app_logger.addHandler(app_logger_handler)
app_logger.setLevel(logging.DEBUG)
app_logger.info("\n****************************************************\n")
app_logger_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s'))
app_logger.info('Запуск сервера сбора данных')

fclt_logger = {}


