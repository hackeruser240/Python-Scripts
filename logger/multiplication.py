import logging 

logger=logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def multiply_nums(x,y):

    if x == 0 or y==0:
        logger.error("Multiplication: One of the numbers is zero")
        return None
    else:
        result=x*y
        logger.info(f"The result of multiplication is {result}")
        return result