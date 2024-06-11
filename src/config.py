import os
from dotenv import load_dotenv
import logging


def setup_logging():
    load_dotenv()
    
    log_dir = os.getenv('LOG_DIR')

    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all messages

    # Create handlers
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)  # Log all messages to the file

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Log only INFO and above to the console

    # Create formatters and add them to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
