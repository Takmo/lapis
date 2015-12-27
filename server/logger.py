import time
import logging

def Logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # file handler that logs everything
    fh = logging.FileHandler('lapis.log')
    fh.setLevel(logging.DEBUG)

    # console handler that only prints warnings and higher
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # make formatter and attach it to handlers
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # attach handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

