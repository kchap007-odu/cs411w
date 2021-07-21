import datetime
import hashlib
import logging
import time


STATUSES = ["on", "off", "timer"]
SOFTWARE_VERSION = datetime.datetime.strptime(
    "2021.07.13", "%Y.%m.%d"
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('SmartDevice.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)
LOGGER.addHandler(fh)
LOGGER.addHandler(ch)


class SmartDevice:
    """The class from which all smart device simulator objects
    will inherit. Parameters common to all smart devices are to be
    defined here.

    Parameters:
    name (str): The user-defined name of the device.
    logger (logging.Logger): The logger to user for logging internal
    events.
    """
    _device_id: str = "0" * 32
    _device_type: str = "none"
    _is_online: bool = True
    _location: str = "none"
    _software_version: datetime.datetime = datetime.datetime.strptime(
        "1970.01.01", "%Y.%m.%d"
    )
    _status: str = "off"
    last_connected: datetime.datetime = 0.0

    def __init__(self, name: str = "unnamed", location: str = "none",
                 device_id: str = None, logger: logging.Logger = LOGGER):
        self._name = name
        self._software_version = SOFTWARE_VERSION
        self.set_location(location)
        self._logger = logger
        if device_id is not None:
            self._device_id = device_id
        else:
            # TODO: Clean this up. Or find a better way to generate
            # unique device id.
            self._device_id = hashlib.md5(
                bytes(str(int(time.time()*1000)), encoding="utf-8")
            ).hexdigest()
        self._logger.debug(
            f"Created device {self._device_id} with name -- "
            + f"{self._name}, software version -- "
            + f"{self._software_version}, "
            + f"location -- {self._location}."
        )

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

    def set_device_id(self, value: str = ""):
        """Setter for device_id.

        Parameters:
        value (str): The value to set device_id to.
        """
        self._device_id = value

    @property
    def device_type(self) -> str:
        """Getter for device type.

        Returns:
        str: the type of the device.
        """
        return self._device_type

    def set_device_type(self, type: str = "none"):
        """Setter for device type.

        Parameters:
        type (str): The type of the device.
        """
        self._device_type = type

    @property
    def location(self) -> str:
        """Getter for location.

        Returns:
        (str): The location of the device.
        """
        return self._location

    def set_location(self, value: str = "none"):
        """Setter for location attribute.

        Parameters:
        value(str): The value to set location to.
        """
        self._location = value

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

    def set_name(self, value: str = ""):
        """Setter method for device name.

        Parameters:
        value (str): The value to set name to.
        """
        self._name = value

    @property
    def software_version(self) -> str:
        """Getter for software version.

        Returns:
        str: The software version.
        """
        return datetime.datetime.strftime(self._software_version)

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
        if status in STATUSES:
            self._logger.info(
                f"Set status of device {self._device_id}"
                + f"to {status}.")
            self._status = status


if __name__ == "__main__":
    pass
