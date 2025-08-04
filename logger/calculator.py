import logging

# Get a logger instance for this specific module
logger = logging.getLogger(__name__)

# Add a NullHandler to prevent "No handlers found" warnings
logger.addHandler(logging.NullHandler())

def divide(x, y):
    """
    Performs division and logs an error if a ZeroDivisionError occurs.
    """
    try:
        result = x / y
        logger.info(f"The result of dividing {x} by {y} is {result}.")
        return result
    except ZeroDivisionError:
        # Log the specific error at the error level
        logger.error("A ZeroDivisionError occurred: Cannot divide by zero.")
        return None