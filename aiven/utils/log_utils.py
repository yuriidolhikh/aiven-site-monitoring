import logging


def get_logger(name, level=logging.DEBUG):
    """Simple shared logger"""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger
