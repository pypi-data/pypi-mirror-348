import logging

logger = logging

logger.basicConfig(
    filename='error-log.txt', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR
)
