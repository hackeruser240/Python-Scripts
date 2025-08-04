import logging
import os

def setup_logger():
    """
    Sets up a logger that writes to a file and the console.
    """
    # Create the logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Define the log file path
    log_file = os.path.join("logs", "logs.txt")
    
    # Create a logger instance
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level

    # Create a file handler for logging to a file
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)  # Set the minimum level for the file

    # Create a console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Set the minimum level for the console

    # Define the log message format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

    # Set the format for both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# --- Example Usage ---

if __name__ == "__main__":
    # Get our configured logger
    logger = setup_logger()

    # Now, you can replace your print() statements with logger calls
    logger.debug("This is a debug message. It will be in the file but not the console.")
    logger.info("This is an info message. It will be in both the file and the console.")
    logger.warning("This is a warning message. It will be in both.")
    logger.error("This is an error message. It will be in both.")
    logger.critical("This is a critical message. It will be in both.")

    # A simple function that might use logging instead of printing
    def calculate_something(x, y):
        logger.debug(f"Calculating the sum of {x} and {y}.")
        if y == 0:
            logger.error("Cannot divide by zero.")
            return None
        result = x + y
        logger.debug(f"The result is {result}.")
        return result

    calculate_something(10, 5)
    calculate_something(10, 0)