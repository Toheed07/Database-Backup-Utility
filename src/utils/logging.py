import logging
from datetime import datetime

# Create and configure the logger
def setup_logger(log_file="backup_utility.log"):
    logger = logging.getLogger("BackupUtilityLogger")
    logger.setLevel(logging.DEBUG)  # Log all levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Show INFO level or higher on the console
    console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Log everything to the file
    file_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
    )
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
