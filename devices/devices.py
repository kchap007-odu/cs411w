import logging
import time

from typing import List, Union

from datetime import datetime

from helpers.misc import create_logger


class SmartDevice:
    """The class from which all smart device simulator objects
    will inherit. Parameters common to all smart devices are to be
    defined here.

    Parameters:
    name (str): The user-defined name of the device.
    logger (logging.Logger): The logger to user for logging internal
    events.
    """
    _device_type: str = "none"
    _api_return_parameters: List = [
        "device_type",
        "name",
        "device_id",
        "software_version",
        "is_online",
        "last_connected"
    ]

    _statuses: List[str] = ["on", "off", "timer"]
    _software_version: datetime = datetime.strptime("2021.07.13", "%Y.%m.%d")

    def __init__(self, name: str = "unnamed", location: str = "none",
                 device_id: Union[str, None] = None,
                 logger: logging.Logger = create_logger()):
        self.set_device_id(device_id)
        self.set_is_online(True)
        self.set_name(name)
        self.set_location(location)
        self._logger: logging.Logger = logger
        self.set_status("off")
        self.set_last_connected(datetime.now())

        self._logger.debug(
            f"Created device {self._device_id} with name -- "
            + f"{self._name}, software version -- "
            + f"{self._software_version}, "
            + f"location -- {self._location}."
        )

    def __api__(self) -> dict:
        """Representation of the object state as a dictionary.

        Returns:
            dict: The state of the device to report in JSON messages.
        """
        self.set_last_connected(datetime.now())
        return self.__as_json__(self._api_return_parameters)

    def __as_json__(self, parameters: List) -> dict:
        """Returns a dictionary of device properties from a list of
        parameter names. Intended to be used with API queries and
        internal state logging.

        Args:
            parameters (List): A list of the property names to return.
        """

        dictionary = {}
        # Comprehensions doesn't work as expected with eval and self
        for parameter in parameters:
            dictionary.update({parameter: eval(f"self.{parameter}")})

        return dictionary

    def __from_json__(self, dictionary: dict):
        """Set device parameters from dictionary. To be used with API
        POST requests and configuration files.

        Args:
            dictionary (dict): The state to set the device to.
        """

        properties = dir(self)
        for key in dictionary.keys():
            parameter = f"set_{key}"
            if parameter in properties:
                eval(f"self.{parameter}(dictionary['{key}'])")
            else:
                self._logger.warning(
                    f"No parameter matching '{parameter}' in object. Skipping")

    def __properties__(self):
        """Getter for settable parameters. Intended to be used to log
        the state of the simulated device to store in a configuration
        file.

        Returns:
            dict: The internal state of the device.
        """
        # FIXME: Make this method more extensible. Maybe regexp?
        parameters = [
            d for d in dir(self) if (d[0] != "_") and (d.count("set") == 0)
        ]

        return self.__as_json__(parameters)

    @property
    def device_id(self) -> str:
        """Getter for unique device identifier.

        Returns:
        str: The unique identifier of the device.
        """
        self._logger.debug(
            f"Get value of device_id for device {self._device_id}"
        )
        return self._device_id

    def set_device_id(self, id_: Union[str, None] = None):
        """Setter for device_id. If device_id is None, a random unique
        id is generated.

        Args:
            device_id (Union[str, None], optional): The value to set
            device_id to. Defaults to None.
        """
        self._device_id = f"{hash(time.time()): X}" if id_ is None else id_

    @property
    def device_type(self) -> str:
        """Getter for device type.

        Returns:
        str: the type of the device.
        """
        return self._device_type

    def set_device_type(self, type_: str = "none"):
        """Setter for device type.

        Parameters:
        type (str): The type of the device.
        """
        self._device_type = type_

    @property
    def is_online(self) -> bool:
        """Getter for is_online

        Returns:
            bool: Whether the device is online. Always returns true.
        """
        return self._is_online

    def set_is_online(self, online: bool = True):
        self._is_online = online

    @property
    def last_connected(self) -> str:
        """Getter for last connected date.

        Returns:
            str: The timestamp of last connection, as iso formmated
            string.
        """
        return self._last_connected.isoformat()

    def set_last_connected(self, date: datetime):
        """Setter for datetime of last connect.

        Args:
            date (datetime): The datetime which the device was last
            connected.
        """
        self._last_connected = date

    @property
    def location(self) -> str:
        """Getter for location.

        Returns:
        (str): The location of the device.
        """
        return self._location

    def set_location(self, location: str = "none"):
        """Setter for location attribute.

        Parameters:
        value(str): The value to set location to.
        """
        self._location = location

    @property
    def name_long(self) -> str:
        """Getter for long name.

        Returns:
        str: The long form name of the smart device.
        """
        return f"{self._name} {self._device_type} ({self._location})"

    @property
    def name(self) -> str:
        """Getter for device name.

        Returns:
        str: The device name.
        """
        return self._name

    def set_name(self, name: str = ""):
        """Setter method for device name.

        Parameters:
        value (str): The value to set name to.
        """
        self._name = name

    @property
    def software_version(self) -> str:
        """Getter for software version.

        Returns:
        str: The software version.
        """
        return datetime.strftime(self._software_version, "%Y.%M.%d")

    @property
    def status(self) -> str:
        """Getter for status.

        Returns:
        str: The current status of the device.
        """
        self._logger.debug(
            f"Get value of status for device {self._device_id}"
        )
        return self._status

    def set_status(self, status: str = "off"):
        """Setter method for status.

        Parameters:
        status (str): The target status of the device. Must be "on",
        "off", or "timer".
        """
        if status in self._statuses:
            self._logger.info(
                f"Set status of device {self._device_id} to {status}.")
            self._status = status
