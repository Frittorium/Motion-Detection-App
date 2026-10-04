import logging

import config

_LOGGER_NAME = "motion_detection"


def initialize_logging() -> logging.Logger:
    logger = logging.getLogger(_LOGGER_NAME)
    level_name = "DEBUG" if config.DEBUG else str(config.LOG_LEVEL).upper()
    logger.setLevel(getattr(logging, level_name, logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(handler)
    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(_LOGGER_NAME)