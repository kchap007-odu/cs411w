from typing import Union

from devices.lights import PhilipsHueLamp
from devices.thermostats import NestThermostat
# from devices.Faucet import Faucet  # Getting invalid syntax error.
from devices.Refrigerator import Refrigerator
from devices.water_heater import water_heater

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
