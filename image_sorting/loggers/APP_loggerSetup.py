from logging.handlers import RotatingFileHandler

import logging
import os
import inspect

def app_loggerSetup():
    # Dynamically get the caller module name
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    module_name = module.__name__ if module else "unknown"

    logger = logging.getLogger(module_name)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)   


        # File handler (unchanged)
        log_path = os.path.join(log_dir, "LOGS-app.log")
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=1_000_000, 
            backupCount=4, 
            encoding="utf-8"
        )


        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
            datefmt="%d-%b-%Y %I:%M %p"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler (new)
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
            datefmt="%d-%b-%Y %I:%M %p"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger