import json
import logging

from typing import List, Union

from devices import Devices, Light, Refrigerator, Thermostat, water_heater

SUPPORTED_DEVICES = Union[
    Devices.SmartDevice,
    Light.PhilipsHueLamp,
    Refrigerator.Refrigerator,
    Thermostat.NestThermostat,
    water_heater.water_heater
]

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


class SmartHome():
    """A class to represent a SmartHome network. Configurations can be
    saved and reloaded through a config file.

    Parameters:
        config_name (str): The name of the configuration file containing
        the smart home configuration.
    """

    def __init__(self, json_file: str = None):
        self._config_name: str = json_file

        self.devices: List[SUPPORTED_DEVICES] = []
        if json_file is not None:
            self._construct_devices_from_json(json_file)

    def _construct_devices_from_json(self, filename: str = ""):
        with open(filename) as f:
            d = json.loads(f.read())
        # FIXME: Rewrite this using dictionary.pop() method.
        if "devices" in d.keys():
            devices = d["devices"]
        for device in devices.keys():
            device_class = devices[device]["class"]
            d = create_class_from_name(device_class)
            d.__from_json__(devices[device])
            self.add_new_device(d)

    def add_new_device(self, device: SUPPORTED_DEVICES = None):
        """Adds a device to the list of devices in the home.

        Args:
            device (SUPPORTED_DEVICES, optional): The device to add.
            Defaults to None.
        """
        self.devices.append(device)

    @property
    def num_devices(self) -> int:
        """Returns the number of devices associated with the smart home.

        Returns:
            int: The number of devices associated with the home.
        """
        return len(self.devices)

    def get_device_by_device_id(self, device_id: str = "") -> SUPPORTED_DEVICES:
        """Gets a device by device ID.

        Args:
            device_id (str, optional): The unique identifier for the
            device. Defaults to "".

        Returns:
            Union[Devices.SmartDevice, Light.PhilipsHueLamp,
            Refrigerator.Refrigerator, Thermostat.NestThermostat,
            water_heater.water_heater, None]: The device matching the
            device ID.
        """
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None

    def get_devices_by_type(self, type_: str = "") -> List:
        """Gets all devices in the smart home matching the device type.

        Args:
            type_ (str, optional): The type of devices to get, e.g.,
            "Light". Defaults to "".

        Returns:
            List: A list of all devices with a matching type
        """
        return [i for i in self.devices if i.device_type == type_]

    def write_config_file(self):
        """Stores the current smart home's device list and states as a
        configuration file.
        """
        dictionary = {}
        for i, device in enumerate(self.devices, start=1):
            dictionary[f"device{i}"] = device.__properties__()

        # print(json.dumps(dictionary, indent=4))


def create_class_from_name(name: str = "") -> SUPPORTED_DEVICES:
    """Helper function to construct supported classes from class names
    stored in the ini file.

    Parameters:
        name (str): The name of the class.
    """
    if name == "NestThermostat":
        return Thermostat.NestThermostat()
    elif name == "PhillipsHueLamp":
        return Light.PhilipsHueLamp()
    elif name == "SmartDevice":
        return Devices.SmartDevice()


if __name__ == "__main__":
    sh = SmartHome(config_name="test-config.ini")
    sh.write_config_file()
