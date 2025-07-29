import logging
import os

logger_cache = {}


def get_global_log_level():
    # Check for an environment variable, fallback to INFO
    return os.environ.get("MUSICGPT_LOG_LEVEL", "INFO").upper()


def get_logger(logger_name, level=None):
    if logger_name in logger_cache:
        return logger_cache[logger_name]

    logger = logging.getLogger(logger_name)

    # Use the provided level, else use the global log level
    level_to_set = level or get_global_log_level()
    level_value = getattr(logging, level_to_set.upper(), logging.INFO)
    logger.setLevel(level_value)
    for handler in logger.handlers:
        handler.setLevel(level_value)

    # If no handlers, add a default StreamHandler
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level_value)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger_cache[logger_name] = logger
    return logger
