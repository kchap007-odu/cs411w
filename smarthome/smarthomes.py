import json
import time

from typing import List, Union

from devices.Light import PhilipsHueLamp
from devices.thermostats import NestThermostat
# from devices.Faucet import Faucet  # Getting invalid syntax error.
from devices.Refrigerator import Refrigerator
from devices.water_heater import water_heater

from helpers.misc import json_from_file

SupportedDevices = Union[
    PhilipsHueLamp,
    Refrigerator,
    NestThermostat,
    # Faucet,
    water_heater
]

SupportedDevicesString = [
    "PhilipsHueLamp",
    "Refrigerator",
    "NestThermostat",
    "Faucet",
    "water_heater"
]


class SmartHome():
    """A class to represent a SmartHome network. Configurations can be
    saved and reloaded through a config file.

    Properties based on Honewell Home response snippets found here:
    https://developer.honeywellhome.com/content/t-series-thermostat-guide

    Parameters:
        json_file (str): The fully qualified path to the file containing
        the configuration data.
    """

    def __init__(self, json_file: str = None):
        # TODO: Need to convert from pascalCase to snake_case on input.
        self.set_location_id(hash(time.time()))
        self.set_name("None")
        self.set_street_address("None")
        self.set_city("None")
        self.set_state("None")
        self.set_country("None")
        self.set_zipcode("None")
        self.set_config_name: Union(str, None) = json_file

        self._devices: List[SupportedDevices] = []

        if json_file is not None:
            json_data = json_from_file(json_file)
            self.__from_json__(json_data)

    def __from_json__(self, json_data: dict):
        # Set up the device properties.
        available_devices = json_data.pop("devices", None)
        if available_devices is not None:
            for v in available_devices.values():
                self.append(device_factory(v.pop("class"), v))

        # Set the home properties.
        properties = dir(self)
        for k in json_data.keys():
            parameter = f"set_{k}"
            if parameter in properties:
                eval(f"self.{parameter}(json_data['{k}'])")

    def __getitem__(self, key: Union[int, str]) -> SupportedDevices:
        if isinstance(key, str):
            # Do search by device id
            for device in self._devices:
                if device.device_id == key:
                    return device
        elif isinstance(key, int):
            return self._devices[key]
        return None

    def __len__(self):
        return len(self._devices)

    def __setitem__(self, key: Union[int, None] = None,
                    value: SupportedDevices = None):
        if key is not None:
            self._devices[key] = value

    def __str__(self):
        dictionary = {}
        for i, device in enumerate(self._devices, start=1):
            dictionary[f"device{i}"] = device.__properties__()

        return json.dumps(dictionary, indent=4)

    def append(self, item: SupportedDevices):
        self._devices.append(item)

    @ property
    def city(self) -> str:
        return self._city

    def set_city(self, city: str):
        self._city = city

    @ property
    def country(self) -> str:
        return self._country

    def set_country(self, country: str):
        self._country = country

    @ property
    def location_id(self) -> str:
        return self._location_id

    def set_location_id(self, location_id: int):
        self._location_id = location_id

    @ property
    def name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    @ property
    def state(self) -> str:
        return self._state

    def set_state(self, state: str):
        self._state = state

    @ property
    def street_address(self) -> str:
        return self._street_address

    def set_street_address(self, street_address: str):
        self._street_address = street_address

    @ property
    def zipcode(self) -> str:
        return self._zipcode

    def set_zipcode(self, zipcode: str):
        self._zipcode = zipcode

    def get_devices_by_type(self, type_: str = "") -> List[SupportedDevices]:
        """Gets all devices in the smart home matching the device type.

        Args:
            type_ (str, optional): The type of devices to get, e.g.,
            "Light". Defaults to "".

        Returns:
            List: A list of all devices with a matching type.
        """
        return [i for i in self._devices if i.device_type == type_]


def device_factory(name: str = "", config: dict = None) -> SupportedDevices:
    """Helper function to construct supported classes from class names
    stored in the ini file.

    Args:
        name (str, optional): The name of the class to create. Defaults
        to "".

    Returns:
        SupportedDevices: The class of device specified by name.
    """
    if name in SupportedDevicesString:
        device = eval(f"{name}()")

    if config is not None:
        device.__from_json__(config)

    return device
