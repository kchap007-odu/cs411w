import configparser
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

    def __init__(self, config_name: str = ""):
        self._config_name: str = config_name

        config = configparser.ConfigParser()
        config.read(config_name)
        self.devices: List[SUPPORTED_DEVICES] = []
        if config.sections():
            self._construct_devices(config)
        else:
            LOGGER.warning("Configuration file is empty")

    def _construct_devices(self, config: configparser.ConfigParser):
        """Constructs devices from a saved configuration in .ini file.
        This function assumes all classes have setters for corresponding
        values following a "set_<name>" format.

        Args:
            config (configparser.ConfigParser): The configuration file
            containing smart device information associated with the
            home.
        """
        for section in config.sections():
            items = dict(config.items(section))
            # TODO: Enforce requirement for class to be in config.
            class_ = items["class"]
            # Remove class since it is not a property of the device.
            del items["class"]
            # Create the device from the stored class name.
            device = create_class_from_name(class_)
            for item in items.keys():
                command = f"device.set_{item}({items[item]})"
                # print(command)
                eval(command)
            self.add_new_device(device)

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
        for i, device in enumerate(self.devices, start=1):
            print(f"[device{i}]")
            params = device.get_settable_parameters()
            for param in params.keys():
                value = f"\"{params[param]}\"" \
                    if isinstance(params[param], str) else f"{params[param]}"
                print(param + "=" + value)


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
