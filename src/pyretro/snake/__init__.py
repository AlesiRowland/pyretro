import logging

snake_logger = logging.getLogger(__name__)
__formatter = logging.Formatter(logging.BASIC_FORMAT)
__handler = logging.StreamHandler()
__handler.setFormatter(__formatter)
snake_logger.addHandler(__handler)


def change_log_level(level):
    snake_logger.setLevel(level)
    snake_logger.setLevel(level)


change_log_level(logging.WARNING)