import logging

LOG_LEVEL = logging.WARNING

handler = logging.StreamHandler()

fmt = logging.Formatter('%(filename)s:%(lineno)d:%(message)s')
handler.setFormatter(fmt)

logger = logging.Logger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)
