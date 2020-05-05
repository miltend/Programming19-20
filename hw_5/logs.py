import logging


def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)
    return log
