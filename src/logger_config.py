import logging
import os


def logger_setting(module_name):
    log_path = os.path.join(os.path.dirname(__file__), "..", "logs", f"{module_name}.log")
    logger = logging.getLogger(module_name)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
    return logger
