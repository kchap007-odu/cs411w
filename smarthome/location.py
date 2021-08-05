import json
import logging
import time

from typing import List, Union

from helpers.factories import SupportedDevices, device_factory
from helpers.misc import create_logger


class Location():
    """A class to represent a location on a Honeywell Home network.
    Configurations can be saved and reloaded through a config file.

    Properties based on Honewell Home response snippets found here:
    https://developer.honeywellhome.com/content/t-series-thermostat-guide

    Parameters:
        json_file (str): The fully qualified path to the file containing
        the configuration data.
    """

    def __init__(self, logger: logging.Logger = None):
        # TODO: Need to convert from pascalCase to snake_case on input.
        self.set_logger(logger)
        self.set_location_id(hash(time.time()))
        self.set_name("None")
        self.set_street_address("None")
        self.set_city("None")
        self.set_state("None")
        self.set_country("None")
        self.set_zipcode("None")

        self._devices: List[SupportedDevices] = []

    def __from_json__(self, json_data: dict):
        """Sets the location information from a JSON-like object.

        Args:
            json_data (dict): The configuration to set.
        """
        # Set up the device properties.
        available_devices = json_data.pop("devices", None)
        if available_devices is not None:
            for config in available_devices:
                device = device_factory(config.pop(
                    "class"), config, self._logger)
                self._devices.append(device)

        # Set the home properties.
        properties = dir(self)
        for k in json_data.keys():
            parameter = f"set_{k}"
            if parameter in properties:
                eval(f"self.{parameter}(json_data['{k}'])")

    def __getitem__(self, key: Union[str, int]) -> SupportedDevices:
        """Getter for items in the collection. Supports indexing by
        array position or keyword.

        Args:
            key (Union[int, str]): The item to get. Addressable in list
            or dictionary syntax.

        Returns:
            SupportedDevices: The device(s) matching the criteria.
        """
        # Search by device id

        if isinstance(key, str) and key in ["Thermostat", "Light", "Plug",
                                            "Refrigerator", "WaterHeater"]:
            return [d for d in self._devices if d.device_type == key]
        elif isinstance(key, str):
            for device in self._devices:
                if device.device_id == key:
                    return device
        # Search by index.
        elif isinstance(key, int):
            return self._devices[key]

        return None

    def __len__(self) -> int:
        """The number of smart devices in this location.

        Returns:
            int: The number of devices.
        """
        return len(self._devices)

    def __to_json__(self) -> dict:
        """A JSON representation of the location object.

        Returns:
            dict: The location information as a JSON-serializable
            dictionary.
        """
        dictionary = {
            "location_id": self.location_id,
            "name": self.name,
            "street_address": self.street_address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "devices": []
        }

        for i, device in enumerate(self._devices, start=1):
            config = device.__properties__()
            config.update(
                {"class": device.__class__.__name__})
            dictionary["devices"].append(config)
        return dictionary

    def __str__(self) -> str:
        """String representation of object.

        Returns:
            str: The object as a string.
        """
        return json.dumps(self.__to_json__(), indent=4)

    def append(self, device: SupportedDevices):
        """Add a new device to the list of devices.

        Args:
            device (SupportedDevices): The device to add.
        """
        self._devices.append(device)

    @ property
    def city(self) -> str:
        """The city that the location is in.

        Returns:
            str: The city.
        """
        return self._city

    def set_city(self, city: str):
        """Setter for city.

        Args:
            city (str): The city of the location.
        """
        self._city = city

    @ property
    def country(self) -> str:
        """The country that the location is in.

        Returns:
            str: The country.
        """
        return self._country

    def set_country(self, country: str):
        """Setter for country.

        Args:
            country (str): The country of the location.
        """
        self._country = country

    @ property
    def location_id(self) -> str:
        """A unique identifier for the location.

        Returns:
            str: The location's unique identifier.
        """
        return self._location_id

    def set_location_id(self, location_id: int):
        """Setter for location_id.

        Args:
            location_id (int): The value to set location_id to.
        """
        self._location_id = location_id

    def set_logger(self, logger: logging.Logger = None):
        """Sets the logger property for the location.

        Args:
            logger (logging.Logger, optional): [description]. Defaults to None.
        """
        if logger is None:
            logger = create_logger(
                filename="smarthome.log", file_log_level=logging.INFO,
                standard_out_log_level=logging.ERROR)
        self._logger = logger

    @ property
    def name(self) -> str:
        """The name of the location.

        Returns:
            str: The name of the location.
        """
        return self._name

    def set_name(self, name: str):
        """Setter for name.

        Args:
            name (str): The value to set name to.
        """
        self._name = name

    @ property
    def state(self) -> str:
        """The location's state.

        Returns:
            str: The state.
        """
        return self._state

    def set_state(self, state: str):
        """Setter for state.

        Args:
            state (str): The value to set state to.
        """
        self._state = state

    @ property
    def street_address(self) -> str:
        """The location's street address.

        Returns:
            str: The street address of the location.
        """
        return self._street_address

    def set_street_address(self, street_address: str):
        """Setter for street_address.

        Args:
            street_address (str): The value to set street address to.
        """
        self._street_address = street_address

    @ property
    def zipcode(self) -> str:
        """The location's zip code.

        Returns:
            str: The zip code.
        """
        return self._zipcode

    def set_zipcode(self, zipcode: str):
        """Setter for zipcode.

        Args:
            zipcode (str): The value to set zipcode to.
        """
        self._zipcode = zipcode
