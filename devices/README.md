# About

The Ener-G View Smart Device Simulator Suite consists of a few
representative smart devices made by popular manufacturers. When
available, the device API was used to model the device. Currently
supported devices are:

- Nest Thermostat
- Phillips Hue Lamp
- Generic Refrigerator
- Generic Plug
- Generic Faucet
- Generic Smart Device

# Creating a new device

Devices inheriting from the device.Devices.SmartDevice class will
inherit the following helper methods:

```
__api__
__as_json__
__from_json__
```

- \_\_api\_\_
  Provides the internal state of the object. Parameters returned will be whatever parameters are specified by the self.\_api_return_parameters property, which
  should be defined at the class level.

- \_\_as_json\_\_
  Provides a method for querying properties of the device from a list of property
  names.

- \_\_from_json\_\_
  Provides a method for setting the internal state of the object from a
  dictionary of values. The structure assumes that subclasses will provide
  getter and setter methods and keep data values "private", or as private
  as Python allows.

An example of setting up a new class inheriting from the base SmartDevice
class can be found in template.py.

# Working with Devices

- Nest Thermostat
  The API can be found here:
  https://developers.nest.com/reference/api-thermostat

- Light
  The API for Phillips Hue Light can be found here:
  https://developers.meethue.com/
  Requires a developer account through sign-up through email.
