import logging
import os
from calculator import divide

def setup_logger():
    """
    Sets up the root logger configuration.
    """
    # Create the logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Define the log file path
    log_file = os.path.join("logs", "logs.txt")
    
    # Configure the root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, mode='w'),
            logging.StreamHandler()
        ]
    )
    
    # Now that logging is configured, we can get a logger instance for this module
    logger = logging.getLogger(__name__)
    return logger

def calculate_something(x, y):
        logger.debug(f"Calculating the sum of {x} and {y}.")
        if y == 0:
            logger.error("Cannot divide by zero.")
            return None
        result = x + y
        logger.debug(f"The result is {result}.")
        return result

if __name__ == "__main__":
    logger = setup_logger()
    
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

    calculate_something(10, 5)
    calculate_something(10, 0)
    
    logger.info("-" * 20)
    logger.info("Demonstrating logging from the 'calculator' module:")
    logger.info("-" * 20)
    
    divide(20, 4)
    divide(10, 0)