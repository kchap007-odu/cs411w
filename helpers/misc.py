import json
import os

from typing import Union

from logging import getLogger, Formatter, FileHandler, StreamHandler, \
    Logger, WARNING, DEBUG, ERROR  # noqa: F401


def create_logger(filename: str = "default_logger.log",
                  file_log_level: int = DEBUG,
                  standard_out_log_level: int = ERROR) -> Logger:
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
    log = getLogger(filename)
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


def log_message_formatter(get_set: str, device_id: str, property_:
                          str, value: Union[str, int] = None) -> str:
    """Formats get and set messages to be written to the log.

    Args:
        get_set (str): Whether variable is being get or set. Must be
        "get" or "set".
        device_id (str): The identifier of the device.
        property_ (str): The name of the property being get/set.
        value (Union[str, int], optional): The value being . Defaults to None.

    Returns:
        str: [description]
    """
    if isinstance(value, str):
        value = f"'{value}'"

    message = f"{get_set} {device_id} {property_}"

    if "set" in get_set:
        message += f" to {value}."
    else:
        message += "."

    return message


def json_from_file(filename: str) -> dict:
    """Reads a .json formatted file and converts the contents to a
    Python dict.

    Args:
        filename (str): The fully qualified path to the file.

    Returns:
        dict: The contents of the specified file as a dictionary.
    """
    with open(filename) as f:
        result = json.loads(f.read())

    return result


def path_relative_to_root(path: str) -> str:
    """Returns the absolute path of a path specified relative to the
    root.

    Args:
        path (str): The root-relative path.

    Returns:
        str: The absolute path to the file.
    """
    return os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", path
            )
        )
    )


def get_device_translations():
    pass
    # with open("")
