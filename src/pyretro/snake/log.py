import logging


def initialise_package_root(package_name):
    _package_root_logger = logging.getLogger(package_name)
    _formatter = logging.Formatter(logging.BASIC_FORMAT)
    _handler = logging.StreamHandler()
    _handler.setFormatter(_formatter)
    _package_root_logger.addHandler(_handler)


class PackageRootLogger:
    def __init__(self, package_name):
        self._logger = logging.getLogger(package_name)
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        self._handler = logging.StreamHandler()
        self._handler.setFormatter(formatter)
        self._logger.addHandler(self._handler)

    def set_level(self, level):
        self._logger.setLevel(level)
        self._handler.setLevel(level)
