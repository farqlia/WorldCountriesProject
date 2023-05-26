import logging
from src.global_vars import LOG_ERRORS_FILE


def log_on_none(logging_level):

    logging_format = '%(levelname)s: %(asctime)s - %(message)s'
    # logging.basicConfig(level=logging_level, format=logging_format)
    file_handler = logging.FileHandler(filename=LOG_ERRORS_FILE)
    file_handler.setFormatter(logging.Formatter(logging_format))
    logger = logging.getLogger()
    logger.addHandler(file_handler)

    def log(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result is None:
                logger.log(level=logging_level, msg=f"{function.__name__}({args, kwargs}) returned None")
            return result
        return wrapper

    return log


log_on_none(logging.WARNING)


def some_none_func(*args, **kwargs):
    return None


if __name__ == "__main__":
    some_none_func(1, 2, "Hello", number=2)