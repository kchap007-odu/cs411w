import logging

from typing import Union

from devices import PhilipsHueLamp, NestThermostat, Refrigerator, \
    SmartPlug, WaterHeater  # noqa: F401
# from devices.water_heater import water_heater

SupportedDevices = Union[
    PhilipsHueLamp,
    Refrigerator,
    NestThermostat,
    SmartPlug,
    WaterHeater
    # Faucet,
    # water_heater
]

SupportedDevicesString = [
    "PhilipsHueLamp",
    "Refrigerator",
    "NestThermostat",
    "SmartPlug",
    "WaterHeater"
    # "Faucet",
    # "water_heater"
]


def device_factory(name: str = "", config: dict = None,
                   logger: logging.Logger = None) -> SupportedDevices:
    """Helper function to construct supported classes from class names
    stored in the ini file.

    Args:
        name (str, optional): The name of the class to create. Defaults
        to "".

    Returns:
        SupportedDevices: The class of device specified by name.
    """
    if name in SupportedDevicesString:
        device = eval(f"{name}(logger=logger)")

    if config is not None:
        device.__from_json__(config)

    return device
