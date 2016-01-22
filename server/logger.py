import time
import logging

def initialize(debug=False):
    # get root logger and set its level
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # file handler that logs everything
    fh = logging.FileHandler('lapis.log')
    fh.setLevel(logging.DEBUG)

    # console handler that only prints warnings and higher
    ch = logging.StreamHandler()
    if debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # make formatter and attach it to handlers
    #formatter = logging.Formatter('[%(asctime)s] [%(name)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M')
    formatter = logging.Formatter('@%(asctime)s [%(name)s] %(levelname)s: %(message)s', datefmt='%s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # attach handlers to root
    root.addHandler(fh)
    root.addHandler(ch)

def get_logger(name='', debug=False):
    # If this is the first time a logger is requested, initialize the root logger with the correct handlers and such
    if (len(logging.getLogger().handlers) is 0):
        initialize(debug)

    # return a child of the root logger with the correct name
    return logging.getLogger(name)

