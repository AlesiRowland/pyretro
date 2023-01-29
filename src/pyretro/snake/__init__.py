import logging

from pyretro.snake.log import PackageRootLogger

log = PackageRootLogger(__name__)
log.set_level(logging.DEBUG)
