# utils/logger.py
import logging
import functools

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

logger = setup_logger()

def log_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Started: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Completed: {func.__name__}")
        return result
    return wrapper