# -*- coding:UTF-8 -*-

import logging
import datetime

class log():

    def __init__(self, log_path):
        # create log basic config
        logging.basicConfig(filename=log_path + '/' + str(datetime.date.today()) + '.log',
                            format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', 
                            level=logging.DEBUG,
                            filemode='a', 
                            datefmt='%Y-%m-%d%I:%M:%S %p')

    def log_event(self, severity, msg):

        if (severity == 10):# DEBUG
            logging.debug(msg)

        elif (severity == 20):# INFO
            logging.info(msg)

        elif (severity == 30):# WARNING
            logging.warning(msg)

        elif (severity == 40):# ERROR
            logging.error(msg)

        elif (severity == 50):# CRITICAL
            logging.critical(msg)
