import sys
from loguru import logger

FMT = '<yellow>{time:MM/D/YYYY HH:mm:ss}</yellow> ' \
      '[<level>{level}</level>] ' \
      ':<cyan>{name}:{function}:{line}</cyan> - ' \
      '<level>{message}</level>'

# supersede the default stderr
logger.remove()
logger.add(sink=sys.stderr, colorize=True, format=FMT, backtrace=True, diagnose=True, enqueue=True)
