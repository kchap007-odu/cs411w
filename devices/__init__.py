# Need __init__.py file to tell Python this is a module.
from devices.lights import PhilipsHueLamp  # noqa: F401
from devices.thermostats import NestThermostat  # noqa: F401
from devices.Refrigerator import Refrigerator  # noqa: F401
from devices.SmartPlug import SmartPlug  # noqa: F401
from devices.water_heater import WaterHeater  # noqa: F401
