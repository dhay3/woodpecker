import sys
from loguru import logger

stderr_fmt = '<yellow>{time:MM/D/YYYY HH:mm:ss}</yellow> ' \
             '[<level>{level}</level>] ' \
             '<green>{thread.name}</green>:<cyan>{name}:{function}:{line}</cyan> - ' \
             '<level>{message}</level>'
# supersede the default stderr
logger.remove()
logger.add(sink=sys.stderr, colorize=True, format=stderr_fmt, backtrace=True, diagnose=True, enqueue=True)

# for testing
# if __name__ == '__main__':
#     logger.debug("That's it, beautiful and simple logging!")
