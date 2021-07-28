# import logging
from logging import getLogger, Formatter, FileHandler, StreamHandler, \
    Logger, WARNING, DEBUG


def create_logger(filename: str = "default_logger.log",
                  file_log_level: int = DEBUG,
                  standard_out_log_level: int = WARNING) -> Logger:
    """Create a logger.

    Args:
        filename (str, optional): The name to give the logger file.
        Defaults to "default_logger.log".
        file_log_level (int, optional): The debug level to print to
        file. Defaults to DEBUG.
        standard_out_log_level (int, optional): The debug level to
        print to standard output. Defaults to WARNING.

    Returns:
        Logger: The logger.
    """
    log = getLogger(__name__)
    log.setLevel(file_log_level)
    formatter = Formatter(
        '%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
    fh = FileHandler(filename)
    fh.setLevel(file_log_level)
    fh.setFormatter(formatter)

    ch = StreamHandler()
    ch.setLevel(standard_out_log_level)
    ch.setFormatter(formatter)
    log.addHandler(fh)
    log.addHandler(ch)

    return log
