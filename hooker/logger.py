import logging
try:
    from configparser import ConfigParser, NoSectionError
except ImportError:
    from configparser import SafeConfigParser as ConfigParser, NoSectionError


config = ConfigParser()
config.read('config.ini')
try:
    LOG_LEVEL = config.get('hooker', 'log_lvl')
    LOG_LEVEL = getattr(logging, LOG_LEVEL, logging.WARNING)
except NoSectionError:
    LOG_LEVEL = logging.WARNING

handler = logging.StreamHandler()

fmt = logging.Formatter('%(filename)s:%(lineno)d:%(message)s')
handler.setFormatter(fmt)

logger = logging.Logger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)
