import locale

from datetime import datetime, timedelta
from typing import List

from devices import Devices


TEMPERATURE_SCALES = ["K", "C", "F"]
HVAC_MODES = ["heat", "cool", "heat-cool", "eco", "off"]
TIMES_TO_TARGET = ["~0", "<5", "~15", "~90", "120"]
TRAINING = ["training", "ready"]
DEGREES_PER_MINUTE = 1
API_RETURN_PARAMETERS = [
    "device_id",
    "name",
    "status",
    "humidity",
    "ambient_temperature",
    "target_temperature",
    "temperature_scale",
    "hvac_mode",
    "fan_timer_timeout"
]


class NestThermostat(Devices.SmartDevice):
    """A smart thermostat class based on the Nest API.

    https://developers.nest.com/reference/api-thermostat
    """
    _device_type = "Thermostat"

    def __init__(self, location: str = "none", name: str = "none"):
        super().__init__(name=name, location=location)
        self.set_temperature_scale("K")
        self.set_fan_timer_duration(minutes=0)
        self.set_eco_temperature_high(0.0)
        self.set_eco_temperature_low(0.0)
        self.set_target_temperature_high(0.0)
        self.set_target_temperature_low(0.0)
        self.set_locked_temp_max(0)
        self.set_locked_temp_min(0)
        self.set_is_locked(False)
        self.set_sunlight_correction_active(False)
        self.set_sunlight_correction_enabled(False)
        self.set_fan_timer_duration()

        self._ambient_temperature: float = 0.0
        self._has_fan: bool = True
        self._humidity: float = 0.0
        # Can't use setter because it expects _hvac_mode to exist.
        self._hvac_mode: str = "off"
        self._locale: str = locale.getlocale()[0]
        # Default is not a valid mode, so must be set this way.
        self._previous_hvac_mode: str = ""
        self._structure_id: str = ""  # Currently unused.
        self._target_temperature: float = 0.0
        self._where_id: str = ""  # Currently unused.
        self._where_name: str = ""  # Currently unused.

        self._logger.debug(
            f"Device {self._device_id} is now a {self._device_type}."
        )

    def _as_dict(self) -> dict:
        """Representation of the object state as a dictionary.

        Returns:
            dict: The state of the device to report in JSON messages.
        """
        self._logger.debug(
            f"Get device {self._device_id} as dictionary."
        )
        return self._dict_from_list(API_RETURN_PARAMETERS)

    def _dict_from_list(self, parameters: List):
        """Returns a dictionary of device properties from a list of
        parameter names. Intended to be used with API queries and
        internal state logging.

        Args:
            parameters (List): A list of the property names to return.
        """

        dictionary = {}
        # Comprehensions doesn't work as expected with eval and self
        for parameter in parameters:
            dictionary.update({parameter: eval(f"self.{parameter}")})

        return dictionary

    def _from_json(self, dictionary: dict):
        """Set device parameters from dictionary. To be used with API
        POST requests and configuration files.

        Args:
            dictionary (dict): The state to set the device to.
        """
        # Look for units first.
        if "temperature_units" in dictionary.keys():
            eval(f"self.set_{dictionary['temperature_units']}")
            # del eval(f"dictionary['temperature_units']")

        properties = dir(self)
        for key in dictionary.keys():
            parameter = f"set_{key}"
            if parameter in properties:
                eval(f"self.{parameter}(dictionary['{key}'])")
            else:
                self._logger.warning(
                    f"No parameter matching '{parameter}' in object. Skipping")

    def _get_settable_parameters(self) -> dict:
        """Getter for settable parameters. Intended to be used to log
        the state of the simulated device to store in a configuration
        file.

        Returns:
            dict: The internal state of the device.
        """
        # TODO: Not sure this is the best way to handle storing the
        # current device state.
        parameters = [
            d for d in dir(self) if (d[0] != "_") and (d.count("set") == 0)
            and (d.count("_c") == 0) and (d.count("_f") == 0)
        ]

        return self._dict_from_list(parameters)

    @ property
    def ambient_temperature(self) -> int:
        """Getter method for ambient temperature.

        Returns:
            int: The current temperature as measured at the device, in
            Kelvin.
        """
        self._logger.debug(
            f"Get value of temperature for device {self._device_id} "
            + f"in units {self._temperature_scale}."
        )
        # TODO: Force this to return an int.
        if self.temperature_scale == "F":
            return self.ambient_temperature_f
        elif self.temperature_scale == "C":
            return self.ambient_temperature_c
        else:
            return self._ambient_temperature

    @ property
    def ambient_temperature_c(self) -> float:
        """Getter for ambient temperature.

        Returns:
            float: The ambient temperature, as measured at the device,
            in Celsius.
        """
        self._logger.debug(
            f"Get ambient temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._ambient_temperature)

    @ property
    def ambient_temperature_f(self) -> float:
        """Getter for ambient temperature in Fahrenheit.

        Returns:
            float: The ambient temperature, as measured at the device,
            in Celsius.
        """
        self._logger.debug(
            f"Get ambient temperature (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.ambient_temperature_c)

    @ property
    def can_heat(self) -> bool:
        """Boolean indicating whether the system controlled by the
        thermostat is capable of heating. For simulation purposes
        this is always true.

        Returns:
            bool: Always true.
        """
        self._logger.debug(
            f"Get heating capability for device {self._device_id}."
        )
        return True

    @ property
    def can_cool(self) -> bool:
        """Boolean indicating whether the system controlled by the
        thermostat is capable of cooling. For simulation purposes
        this is always true.

        Returns:
            bool: Always true.
        """
        self._logger.debug(
            f"Get cooling capability for device {self._device_id}."
        )
        return True

    @ property
    def eco_temperature_high_f(self) -> float:
        """Getter for the target high temperature, in Fahrenheit.

        Returns:
            float: The high eco temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get high eco temperature (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.eco_temperature_high_c)

    @ property
    def eco_temperature_high_c(self) -> float:
        """Getter for the target high eco temperature, in Celsius.

        Returns:
            float: The high eco temperature, in Celsius.
        """
        self._logger.debug(
            f"Get high eco temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._eco_temperature_high)

    @ property
    def eco_temperature_high(self) -> int:
        """Getter for eco temperature.

        Returns:
            int: The eco temperature in current units.
        """
        # TODO: Force this to return an int.
        if self.temperature_scale == "C":
            return self.eco_temperature_high_c
        elif self.temperature_scale == "F":
            return self.eco_temperature_high_f
        else:
            return self._eco_temperature_high

    def set_eco_temperature_high(self, value: int = 0):
        """Setter for high eco temperature value. Assumes set units are
        the same as the current system units.

        Args:
            value (int, optional): The temperature to set the high eco
            value to. Defaults to 0.
        """
        if self._temperature_scale == "F":
            self._eco_temperature_high = celsius_to_kelvin(
                fahrenheit_to_celsius(value)
            )
        elif self._temperature_scale == "C":
            self._eco_temperature_high = celsius_to_kelvin(value)
        else:
            self._eco_temperature_high = value

    @ property
    def eco_temperature_low_f(self) -> float:
        """Getter for the target low eco temperature, in Fahrenheit.

        Returns:
            float: The low eco temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get low eco temperature (F) for device {self._device_id}"
        )
        return celsius_to_fahrenheit(self.eco_temperature_low_c)

    @ property
    def eco_temperature_low_c(self) -> float:
        """Getter for the target low eco temperature, in Celsius.

        Returns:
            float: The high eco temperature, in Celsius.
        """
        self._logger.debug(
            f"Get low eco temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._eco_temperature_low)

    @ property
    def eco_temperature_low(self) -> int:
        """Getter for the target low eco temperature.

        Returns:
            int: The eco low temperature, in current units.
        """
        # TODO: Force this to return an int.
        if self.temperature_scale == "C":
            return self.eco_temperature_low_c
        elif self.temperature_scale == "F":
            return self.eco_temperature_low_f
        else:
            return self._eco_temperature_low

    def set_eco_temperature_low(self, value: int = 0):
        """Setter for low eco temperature value. Assumes set units are
        the same as the current system units.

        Args:
            value (int, optional): The temperature to set the low eco
            value to. Defaults to 0.
        """
        if self._temperature_scale == "F":
            self._eco_temperature_low = celsius_to_kelvin(
                fahrenheit_to_celsius(value)
            )
        elif self._temperature_scale == "C":
            self._eco_temperature_low = celsius_to_kelvin(value)
        else:
            self._eco_temperature_low = value

    @ property
    def fan_timer_active(self) -> bool:
        """Boolean indicating whether the fan timer is active.

        Returns:
            bool: True if fan timer is active, false otherwise.
        """
        self._logger.debug(
            f"Get fan timer active status for device {self._device_id}."
        )
        return self.fan_timer_timeout > datetime.now()

    @ property
    def fan_timer_timeout(self) -> datetime:
        """The time at which the fan timer will reach zero.

        Returns:
            datetime.datetime: The time at which the fan will become
            inactive.
        """
        self._logger.debug(
            f"Get fan timer timeout for device {self._device_id}."
        )
        return datetime.now() + self.fan_timer_duration

    @ property
    def fan_timer_duration(self) -> timedelta:
        """Getter for fan timer duration.

        Returns:
            datetime.datetime: The fan timer duration.
        """
        self._logger.debug(
            f"Get fan timer duration for device {self._device_id}."
        )
        return self._fan_timer_duration

    def set_fan_timer_duration(self, minutes: int = 5):
        """Setter for fan timer duration.

        Args:
            value (int, optional): The duration, in minutes, to set the
            fan timer. Defaults to 5.
        """
        self._fan_timer_duration = timedelta(minutes=minutes)
        self._logger.info(
            f"Set timeout for device {self._device_id} to {minutes} "
            + f"mintues (datetime value {self._fan_timer_duration}."
        )

    @ property
    def has_fan(self) -> bool:
        """Boolean indicating whether the system controlled by the
        thermostat has a fan. For simulation purposes this is
        always true.

        Returns:
            bool: Always true.
        """
        self._logger.debug(f"Get fan status for device {self._device_id}.")
        return True

    def set_has_fan(self, value: bool = True):
        """Setter for has_fan property.

        Args:
            value (bool, optional): The value to set has_fan to.
            Defaults to True.
        """
        self._has_fan = value

    @ property
    def has_leaf(self) -> bool:
        """Boolean indicating whether the device is set to
        energy-saving temperature.

        Returns:
            bool: Whether thermostat is in energy saving mode.
        """
        self._logger.debug(f"Get leaf status for device {self._device_id}.")
        return self._hvac_mode == "eco"

    @ property
    def humidity(self) -> float:
        """Returns the humidity measured by the thermostat as a
        percentage between 0 and 1.

        Returns:
            float: Percentage humidity, between 0 and 1 inclusive.
        """
        self._logger.debug(
            f"Get value of humidity for device {self._device_id}."
        )
        return self._humidity

    @ property
    def hvac_mode(self) -> str:
        """Getter for the current HVAC mode.

        Returns:
            str: The current HVAC mode.
        """
        self._logger.debug(f"Get HVAC mode for device {self._device_id}.")
        return self._hvac_mode

    def set_hvac_mode(self, value: str = "off"):
        """Setter for the HVAC mode.

        Args:
            value (str, optional): The value to set HVAC mode to. Must
            be "cool", "heat", "heat-cool", or "off". Defaults to "off".
        """
        if value in HVAC_MODES:
            self.set_previous_hvac_mode(self._hvac_mode)
            self._logger.info(
                f"Set HVAC mode of device {self._device_id} to {value}."
            )
            self._hvac_mode = value
        else:
            self._logger.warning(
                f"Device {self._device_id} hvac_mode "
                + f"cannot take a value of {value}"
            )

    @ property
    def is_cooling(self) -> bool:
        """Boolean indicating whether the system is actively cooling.

        Returns:
            bool: True if current temperature is greater than target
            temperature.
        """
        self._logger.debug(f"Get cooling status of device {self._device_id}.")
        return (self._ambient_temperature > self._target_temperature) \
            and self.can_cool \
            and (self._hvac_mode == "cool" or self._hvac_mode == "heat-cool")

    @ property
    def is_heating(self) -> bool:
        """Boolean indicating whether the system is actively heating.

        Returns:
            bool: True if current temperature is less than target
            temperature.
        """
        self._logger.debug(f"Get heating status of device {self._device_id}.")
        return (self._ambient_temperature < self._target_temperature) \
            and self.can_heat \
            and (self._hvac_mode == "heat" or self._hvac_mode == "heat-cool")

    @ property
    def is_locked(self) -> bool:
        """Getter for locked status of the device.

        Returns:
            bool: Whether the device is locked.
        """
        self._logger.debug(f"Get locked status of device {self._device_id}")
        return self._is_locked

    def set_is_locked(self, value: bool = False):
        """Setter for is_locked.

        Args:
            value (bool, optional): The desired lock status of the
            device. Defaults to False.
        """
        self._is_locked = value
        self._logger.debug(
            f"Set locked status of device {self._device_id} to {value}."
        )

    @ property
    def is_using_emergency_heat(self) -> bool:
        """Boolean indicating whether the system controlled by the
        themostat is using emergency heat.

        Returns:
            bool: Whether the emergency heat is active.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(
            f"Get emergency heat status of device {self._device_id}"
        )
        return False

    @ property
    def label(self) -> str:
        """Getter method for user-settable device label.

        Returns:
            str: The device label.
        """
        self._logger.debug(f"Get label for device {self._device_id}.")
        return self._name

    def set_label(self, value: str = "nowhere"):
        """Setter for device label.

        Args:
            value (str, optional): The value to set the label to.
            Defaults to "nowhere".
        """
        self._logger.info(
            f"Set value of label for device {self._device_id} to {value}."
        )
        self._name = value

    @ property
    def locale(self) -> str:
        """Getter for locale.

        Returns:
            str: The current locale being used by the device.
        """
        self._logger.debug(
            f"Get value of locale for device {self._device_id}."
        )
        return self._locale

    @ property
    def locked_temp_max_c(self) -> float:
        """Getter for locked max temperature, in Celsius.

        Returns:
            float: The locked maximum temperature, in Celsius.
        """
        self._logger.debug(
            f"Get locked temp (C) max status for device {self._device_id}."
        )
        return kelvin_to_celsius(self._locked_temp_max)

    @ property
    def locked_temp_max_f(self) -> float:
        """Getter for locked max temperature, in Fahrenheit.

        Returns:
            float: The locked maximum temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get locked temp (F) max for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.locked_temp_max_c)

    @ property
    def locked_temp_max(self) -> int:
        """Getter for locked temperature.

        Returns:
            int: The locked temperature, in current units.
        """
        # TODO: Force this to return an int.
        if self.temperature_scale == "C":
            return self.locked_temp_max_c
        elif self.temperature_scale == "F":
            return self.locked_temp_max_f
        else:
            return self._locked_temp_max

    def set_locked_temp_max(self, value: int = 0):
        """Setter for high locked temperature value. Assumes set units
        are the same as the current system units.

        Args:
            value (int, optional): The temperature to set the high
            locked value to. Defaults to 0.
        """
        if self._temperature_scale == "F":
            self._locked_temp_max = celsius_to_kelvin(
                fahrenheit_to_celsius(value)
            )
        elif self._temperature_scale == "C":
            self._locked_temp_max = celsius_to_kelvin(value)
        else:
            self._locked_temp_max = value

    @ property
    def locked_temp_min_c(self) -> float:
        """Getter for locked min temperature, in Celsius.

        Returns:
            float: The locked minimum temperature, in Celsius.
        """
        self._logger.debug(
            f"Get locked temp (C) min status for device {self._device_id}."
        )
        return kelvin_to_celsius(self._locked_temp_min)

    @ property
    def locked_temp_min_f(self) -> float:
        """Getter for locked min temperature, in Fahrenheit.

        Returns:
            float: The locked minimum temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get locked temp (F) min for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.locked_temp_min_c)

    @ property
    def locked_temp_min(self) -> int:
        """Getter for locked temp min.

        Returns:
            int: The minimum locked temperature, in current units.
        """
        # TODO: Force this to return an int.
        if self.temperature_scale == "C":
            return self.locked_temp_min_c
        elif self.temperature_scale == "F":
            return self.locked_temp_min_f
        else:
            return self._locked_temp_min

    def set_locked_temp_min(self, value: int = 0):
        """Setter for high locked temperature value. Assumes set units
        are the same as the current system units.

        Args:
            value (int, optional): The temperature to set the high
            locked value to. Defaults to 0.
        """
        if self._temperature_scale == "F":
            self._locked_temp_min = celsius_to_kelvin(
                fahrenheit_to_celsius(value)
            )
        elif self._temperature_scale == "C":
            self._locked_temp_min = celsius_to_kelvin(value)
        else:
            self._locked_temp_min = value

    @ property
    def previous_hvac_mode(self) -> str:
        """Getter for previous HVAC mode.

        Returns:
            str: The HVAC mode previous to the current.
        """
        self._logger.debug(
            f"Get previous HVAC mode for device {self._device_id}."
        )
        return self._previous_hvac_mode

    def set_previous_hvac_mode(self, value: str):
        """Setter for previous hvac mode.

        Args:
            value(str): The value to set previous hvac mode to.
        """

        if value in HVAC_MODES:
            self._logger.info(
                "Set previous HVAC mode of device "
                + f"{self._device_id} to {value}."
            )
            self._previous_hvac_mode = value

    @ property
    def sunlight_correction_enabled(self) -> bool:
        """Getter for sunlight correction enabled.

        Returns:
            bool: Whether sunlight correction is enabled.
        """
        self._logger.debug(
            "Get sunlight correction enable "
            + f"status for device {self._device_id}."
        )
        return self._sunlight_correction_enabled

    def set_sunlight_correction_enabled(self, value: bool = False):
        """Setter for sunlight correction enable.

        Args:
            value (bool, optional): The value to set sunlight correction
            to. Defaults to False.
        """
        self._sunlight_correction_enabled = value

    @ property
    def sunlight_correction_active(self) -> bool:
        """Getter for sunlight correction active.

        Returns:
            bool: Whether the sunlight correction is active.
        """
        self._logger.debug(
            "Get sunlight correction active "
            + f"status for device {self._device_id}."
        )
        return self._sunlight_correction_active

    def set_sunlight_correction_active(self, value: bool = False):
        """Setter for sunlight correction active status.

        Args:
            value (bool, optional): Value to set sunlight correction
            status to. Defaults to False.
        """
        self._sunlight_correction_active = value

    @ property
    def target_temperature(self) -> int:
        """Selects the appropriate target temperature based on HVAC mode
        and temperature scale.

        Returns:
            int: The target temperature in units specified by
            temperature scale.
        """
        # TODO: Force this to return an int.
        # TODO: Find a better way to do this. This is ugly.
        if self._hvac_mode == "cool":
            return self.target_temperature_low
        elif self._hvac_mode == "heat":
            return self.target_temperature_high
        elif self._hvac_mode == "heat-cool":
            # TODO: Fix this so that heat or cool is chosen.
            if self.ambient_temperature_c > self.target_temperature_c:
                return self.target_temperature_low
            elif self.ambient_temperature_c < self.target_temperature_c:
                return self.target_temperature_high
        elif self._hvac_mode == "eco":
            if self.ambient_temperature_c > self.target_temperature_c:
                return self.eco_temperature_low
            elif self.ambient_temperature_c < self.target_temperature_c:
                return self.eco_temperature_high

    @ property
    def target_temperature_f(self) -> float:
        """Getter for target temperature.

        Returns:
            float: The target temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.target_temperature_c)

    @ property
    def target_temperature_c(self) -> float:
        """Getter for target temperature, in Celsius.

        Returns:
            float: The target temperature, in Celsius.
        """
        self._logger.debug(
            f"Get target temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._target_temperature)

    @ property
    def target_temperature_high(self) -> int:
        """Getter for the target high temperature.

        Returns:
            int: The target high temperature, in current units.
        """
        # TODO: Force this to return an int.
        if self.temperature_scale == "C":
            return self.target_temperature_high_c
        elif self.temperature_scale == "F":
            return self.target_temperature_high_f
        else:
            return self._target_temperature_high

    @ property
    def target_temperature_high_f(self) -> float:
        """Getter for the target high temperature, in Fahrenheit.

        Returns:
            float: The target high temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature high (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.target_temperature_high_c)

    @ property
    def target_temperature_high_c(self) -> float:
        """Getter for the target high temperature, in Celsius.

        Returns:
            float: The target high temperature, in Celsius.
        """
        self._logger.debug(
            f"Get target temperature high (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._target_temperature_high)

    def set_target_temperature_high(self, value: int = 0):
        """Setter for high temperature value. Assumes set units are
        the same as the current system units.

        Args:
            value (int, optional): The temperature to set the high
            temperature value to. Defaults to 0
        """
        if self._temperature_scale == "F":
            self._target_temperature_high = celsius_to_kelvin(
                fahrenheit_to_celsius(value)
            )
        elif self._temperature_scale == "C":
            self._target_temperature_high = celsius_to_kelvin(value)
        else:
            self._target_temperature_high = value

    @ property
    def target_temperature_low_f(self) -> float:
        """Getter for the target low temperature, in Fahrenheit.

        Returns:
            float: The target low temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature low (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.target_temperature_low_c)

    @ property
    def target_temperature_low_c(self) -> float:
        """Getter for the target low temperature, in Fahrenheit.

        Returns:
            float: The target low temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature low (C) for device {self._device_id}"
        )
        return kelvin_to_celsius(self._target_temperature_low)

    def set_target_temperature_low(self, value: int = 0):
        """Setter for low target temperature value. Assumes set units
        are the same as the current system units.

        Args:
            value (int, optional): The temperature to set the low target
            temperature value to. Defaults to 0.
        """
        if self._temperature_scale == "F":
            self._target_temperature_low = celsius_to_kelvin(
                fahrenheit_to_celsius(value)
            )
        elif self._temperature_scale == "C":
            self._target_temperature_low = celsius_to_kelvin(value)
        else:
            self._target_temperature_low = value

    @ property
    def target_temperature_low(self) -> int:
        """Getter for target low temperature.

        Returns:
            int: The target low temperature, in current units.
        """
        # TODO: Force this to return an int.
        if self.temperature_scale == "C":
            return self.target_temperature_low_c
        elif self.temperature_scale == "F":
            return self.target_temperature_low_f
        else:
            return self._target_temperature_low

    @ property
    def temperature_scale(self) -> str:
        """Getter method for units.

        Returns:
            str: Current temperature units returned by the device.
        """
        self._logger.debug(f"Get value of units for device {self._device_id}.")
        return self._temperature_scale

    def set_temperature_scale(self, scale: str = "K"):
        """Setter for units.

        Args:
            scale (str, optional): The target units. Must be "K", "C",
            or "F". Defaults to "K".
        """
        if scale in TEMPERATURE_SCALES:
            self._logger.info(
                f"Set value of scale for device {self._device_id} to {scale}."
            )
            self._temperature_scale = scale

    @ property
    def time_to_target(self) -> str:
        """Calculates the time, in minutes, for the structure to reach
        the target temperature.

        Returns:
            str: A string representation of the estimated time.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(
            f"Get value of time to target for device {self._device_id}."
        )
        return TIMES_TO_TARGET[0]

    @ property
    def time_to_target_training(self) -> str:
        """Getter for the time-to-temperature training mode.

        Returns:
            str: The training mode.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(
            "Get value of time to target training "
            + "for device {self._device_id}."
        )
        return TRAINING[0]


def kelvin_to_celsius(value: float = 0) -> float:
    """Converts a value from Kelvin temperature scale to Celsius
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Celsius.
    """
    return value - 273.15


def celsius_to_kelvin(value: float = 0) -> float:
    """Converts a value from Celsius temperature scale to Kelvin
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Kelvin.
    """
    return value + 273.15


def celsius_to_fahrenheit(value: float = 0) -> float:
    """Converts a value from Celsius temperature scale to Fahrenheit
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Fahrenheit.
    """
    return value * (9/5) + 32


def fahrenheit_to_celsius(value: float = 0) -> float:
    """Converts a value from Fahrenheit temperature scale to Celsius
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Celsius.
    """
    return (value - 32) * (5/9)
