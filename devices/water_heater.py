import random
import logging
import time

from devices.devices import SmartDevice

from typing import List

# class WaterHeater inherits from SmartDevice
# Class variables
# ---------------
# List of supported units
# Current Temperature in standard unit
# Volume of water that heater can hold
# Status (is on or off?)

# Class constructors
# -----------------
# Set values of class variables including inherited variables from SmartDevice

# Class methods
# -------------
# Get temp in given supported unit
# Turn on
# Heat up water
# Cool down water
# Turn off

class: WaterHeater:

""" A smart waterheater class based on the NesThermostat class"""

    _device_type: str= "Waterheater"
    _temperature_scales: List = ["K", "C", "F"]
    _heater_modes: List[str] = ["Hot", "cold", "off"]
    _return_parameters: List = [
        "device_id",
        "device_type",
        "name",
        "status",
        "ambient_temperature",
        "target_temperature",
        "heater_mode"
    ]
    _statuses: List[str] = ["on", "off"]

    def __init__(Self, location: str = "none", name: str = "none", device_id: str = None, logger: logging.Logger = None):
            super(). __init__(name =name, logger=logger, device_id=device_id)


self.set_logger(logger)
self.set_device_id(device_id)
self.set_is_online(True)
self.set_name(name)
self.set_location(location)
self.set_software_version(self._software_version_string)
self.set_status("off")
self.set_last_connected(datetime.now().isoformat())

self._logger.debug(
    f"create {self} name -- "
    + f"{self.name}, software_version -- "
    + f"{self.software_version}, "
    + f"location -- {self.location}."
)


def __getitem__(self, key: str):
    return eval(f"self.{key}") if key in dir(self) else None


def __api__(self) -> dict:

    self.set_last_connected(datetime.now().isoformat())
    return self.__as_json__(self._api_return_parameters)


def __as_json__(self, parameters: List) -> dict:


    dictionary = {}
    # Comprehensions doesn't work as expected with eval and self
    for parameter in parameters:
        dictionary.update({parameter: eval(f"self.{parameter}")})

    return dictionary


def __from_json__(self, dictionary: dict):

    for key in dictionary.keys():
        parameter = f"set_{key}"
        if parameter in dir(self):
            eval(f"self.{parameter}(dictionary['{key}'])")
        else:
            self._logger.warning(
                f"abort set -- '{parameter}' not in {self.device_type}")

@property
def device_id(self) -> str:

    self._logger.debug("get device_id.")
    return self._device_id


def set_device_id(self, id_: Union[str, None] = None):
    self._device_id = f"{hash(time.time()):016X}" if id_ is None else id_


@property
def device_type(self) -> str:
    return self._device_type


def set_device_type(self, type_: str = "none"):
    self._logger.info(f"{self} is now a {type_}.")
    self._device_type = type_


@property
def is_online(self) -> bool:
    return self._is_online


def set_is_online(self, online: bool = True):
    self._is_online = online
    self._logger.info(log_message_formatter(
        "set", f"{self}", "is_online", online))

@property
def location(self) -> str:
    self._logger.debug(log_message_formatter("get", f"{self}", "location"))
    return self._location


def set_location(self, location: str = "none"):
    self._logger.info(log_message_formatter(
        "set", f"{self}", "location", location))
    self._location = location


def set_logger(self, logger: logging.Logger = None):
    if logger is None:
        logger: logging.Logger = create_logger()
        self._logger.warning("Using default logger.")
    self._logger = logger
    self._logger.info("set logger.")


@property
def name_long(self) -> str:

    self._logger.debug(log_message_formatter(
        "get", f"{self}", "name_long"))
    return f"{self._name} {self._device_type} ({self._location})"


@property
def name(self) -> str:

    self._logger.debug(log_message_formatter(
        "get", f"{self}", "name"))
    return self._name


def set_name(self, name: str = ""):
    self._name = name
    self._logger.info(log_message_formatter(
        "set", f"{self}", "name", name))


@property
def status(self) -> str:
    self._logger.debug(log_message_formatter("get", f"{self}", "status"))
    return self._status


def set_status(self, status: str = "off"):
    if status in self._statuses:
        self._status = status
        self._logger.info(log_message_formatter(
            "set", f"{self}", "status", self._status))
    else:
        self._logger.warning(
            f"abort set {self} status -- not in {self._statuses}.")



""" 
Alternate version - not used 
#temperature of hot water
th = 140

#temperature of input cold water
#generated randomly
tc = random.randint(60,81)
#print (random.randint(60,81))

#performance ratio
pr = 0.9

#volume

print("Enter the capacity of water heater")
string = input()

print(string)

v = float(string)

#string = input("Enter the capacity of water heater")

#Specific heat of water
c = 4.187


deltaT = th-tc

#energy in kWh
E = 0
"""


'''
Formula to find the total energy:
E = C*V*DeltaT/PR

Where E = energy in kWh

C = Specific heat of water - 4.187 kJ/kgK, or 1,163 Wh/kg°C

V = volume of water to heat

deltaT = Th-Tc

Th = temperature of hot water

Tc = temperature of input cold water
'''