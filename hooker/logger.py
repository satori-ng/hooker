import logging
from configparser import SafeConfigParser


config = SafeConfigParser()
config.read('config.ini')
LOG_LEVEL = config.get('hooker', 'log_lvl')
LOG_LEVEL = getattr(logging, LOG_LEVEL, logging.ERROR)

handler = logging.StreamHandler()

fmt = logging.Formatter('%(filename)s:%(lineno)d:%(message)s')
handler.setFormatter(fmt)

logger = logging.Logger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)
