import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    # Console logging configuration
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File logging configuration
    file_handler = TimedRotatingFileHandler('btb_app.log', when='D', interval=10, backupCount=2)
    file_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Handlers
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
