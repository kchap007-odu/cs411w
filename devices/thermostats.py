import locale
import logging

from datetime import datetime, timedelta
from typing import List

from devices.devices import SmartDevice

from helpers.unitconverters import celsius_to_fahrenheit, celsius_to_kelvin, \
    fahrenheit_to_celsius, kelvin_to_celsius
from helpers.misc import log_message_formatter


class NestThermostat(SmartDevice):
    """A smart thermostat class based on the Nest API.

    https://developers.nest.com/reference/api-thermostat
    """
    _device_type: str = "Thermostat"
    _temperature_scales: List = ["K", "C", "F"]
    _hvac_modes: List[str] = ["heat", "cool", "heat-cool", "eco", "off"]
    _time_to_target_options: List[str] = ["~0", "<5", "~15", "~90", "120"]
    _training_modes: List[str] = ["training", "ready"]
    _degrees_per_minute: int = 1  # Currently unused.
    _api_return_parameters: List = [
        "device_id",
        "device_type",
        "name",
        "status",
        "humidity",
        "ambient_temperature",
        "target_temperature",
        "temperature_scale",
        "hvac_mode",
        "fan_timer_timeout"
    ]

    def __init__(self, location: str = "none", name: str = "none",
                 device_id: str = None, logger: logging.Logger = None):
        super().__init__(name=name, location=location, logger=logger,
                         device_id=device_id)
        self.set_temperature_scale("K")
        self.set_fan_timer_duration()
        self.set_fan_timer_timeout()
        self.set_eco_temperature_high(0.0)
        self.set_eco_temperature_low(0.0)
        self.set_target_temperature_high(0.0)
        self.set_target_temperature_low(0.0)
        self.set_locked_temp_max(0)
        self.set_locked_temp_min(0)
        self.set_is_locked(False)
        self.set_sunlight_correction_active(False)
        self.set_sunlight_correction_enabled(False)

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

        self._api_return_parameters = self._api_return_parameters + \
            super()._api_return_parameters

    def __properties__(self) -> dict:
        """Getter for settable parameters. Intended to be used to log
        the state of the simulated device to store in a configuration
        file.

        Returns:
            dict: The internal state of the device.
        """
        parameters = [
            d for d in dir(self) if (d[0] != "_") and (d.count("set") == 0)
            and (d.count("_c") == 0) and (d.count("_f") == 0)
        ]

        return self.__as_json__(parameters)

    def __from_json__(self, properties: dict):
        """Set device parameters from dictionary. To be used with API
        POST requests and configuration files.

        Args:
            dictionary (dict): The state to set the device to.
        """
        # Look for units first so the temperatures are set correctly.
        value = properties.pop("temperature_scale", None)
        if value is not None:
            eval(f"self.set_temperature_scale('{value}')")

        # Let superclass handle the rest
        super().__from_json__(properties)

    @property
    def ambient_temperature(self) -> int:
        """Getter method for ambient temperature.

        Returns:
            int: The current temperature as measured at the device, in
            Kelvin.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "ambient_temperature"))
        # TODO: Force this to return an int.
        if self.temperature_scale == "F":
            return self.ambient_temperature_f
        elif self.temperature_scale == "C":
            return self.ambient_temperature_c
        else:
            return self._ambient_temperature

    @property
    def ambient_temperature_c(self) -> float:
        """Getter for ambient temperature.

        Returns:
            float: The ambient temperature, as measured at the device,
            in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "ambient_temperature_c"))
        return kelvin_to_celsius(self._ambient_temperature)

    @property
    def ambient_temperature_f(self) -> float:
        """Getter for ambient temperature in Fahrenheit.

        Returns:
            float: The ambient temperature, as measured at the device,
            in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "ambient_temperature_f"))
        return celsius_to_fahrenheit(self.ambient_temperature_c)

    @property
    def can_heat(self) -> bool:
        """Boolean indicating whether the system controlled by the
        thermostat is capable of heating. For simulation purposes
        this is always true.

        Returns:
            bool: Always true.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "can_heat"))
        return True

    @property
    def can_cool(self) -> bool:
        """Boolean indicating whether the system controlled by the
        thermostat is capable of cooling. For simulation purposes
        this is always true.

        Returns:
            bool: Always true.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "can_cool"))
        return True

    @property
    def eco_temperature_high_f(self) -> float:
        """Getter for the target high temperature, in Fahrenheit.

        Returns:
            float: The high eco temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "eco_temperature_high_f"))
        return celsius_to_fahrenheit(self.eco_temperature_high_c)

    @property
    def eco_temperature_high_c(self) -> float:
        """Getter for the target high eco temperature, in Celsius.

        Returns:
            float: The high eco temperature, in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "eco_temperature_high_c"))
        return kelvin_to_celsius(self._eco_temperature_high)

    @property
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

        self._logger.debug(log_message_formatter(
            "get", f"{self}", "eco_temperature_high"))

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
        self._logger.info(log_message_formatter(
            "set", f"{self}", "eco_temperature_high",
            f"{value} {self.temperature_scale}"))

    @property
    def eco_temperature_low_f(self) -> float:
        """Getter for the target low eco temperature, in Fahrenheit.

        Returns:
            float: The low eco temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "eco_temperature_low_f"))
        return celsius_to_fahrenheit(self.eco_temperature_low_c)

    @property
    def eco_temperature_low_c(self) -> float:
        """Getter for the target low eco temperature, in Celsius.

        Returns:
            float: The high eco temperature, in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "eco_temperature_low_c"))
        return kelvin_to_celsius(self._eco_temperature_low)

    @property
    def eco_temperature_low(self) -> int:
        """Getter for the target low eco temperature.

        Returns:
            int: The eco low temperature, in current units.
        """
        # TODO: Force this to return an int or float rounded to 0.5.
        if self.temperature_scale == "C":
            return self.eco_temperature_low_c
        elif self.temperature_scale == "F":
            return self.eco_temperature_low_f
        else:
            return self._eco_temperature_low

        self._logger.debug(log_message_formatter(
            "get", f"{self}", "eco_temperature_low"))

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

        self._logger.info(log_message_formatter(
            "set", f"{self}", "eco_temperature_low",
            f"{value} {self.temperature_scale}"))

    @property
    def fan_timer_active(self) -> bool:
        """Boolean indicating whether the fan timer is active.

        Returns:
            bool: True if fan timer is active, false otherwise.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "fan_timer_active"))
        return datetime.fromisoformat(self.fan_timer_timeout) > datetime.now()

    @property
    def fan_timer_timeout(self) -> str:
        """The time at which the fan timer will reach zero.

        Returns:
            str: The time at which the fan will become inactive.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "fan_timer_timeout"))
        return self._fan_timer_timeout.isoformat()

    def set_fan_timer_timeout(self, time_: str = None):
        """Set the fan timer timeout to current time plus fan timer
        duration. If no time is provided, the timeout will be set to
        current time plus fan timer duration.

        Args:
            time_ (str, optional): The time to set the fan timer timeout
            to. Expects isoformat time. If no input. Defaults to None.
        """
        if time_ is not None:
            self._fan_timer_timeout = datetime.fromisoformat(time_)
        else:
            self._fan_timer_timeout = datetime.now() + self._fan_timer_duration

        self._logger.info(log_message_formatter(
            "set", f"{self}", "fan_timer-timeout", self.fan_timer_timeout))

    @property
    def fan_timer_duration(self) -> int:
        """Getter for fan timer duration.

        Returns:
            int: The fan timer duration, in minutes.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "fan_timer_duration"))
        return self._fan_timer_duration.seconds / 60

    def set_fan_timer_duration(self, minutes: int = 5):
        """Setter for fan timer duration.

        Args:
            value (int, optional): The duration, in minutes, to set the
            fan timer. Defaults to 5.
        """
        self._fan_timer_duration = timedelta(minutes=minutes)
        self._logger.info(log_message_formatter(
            "set", f"{self}", "fan_timer_duration", minutes))

    @property
    def has_fan(self) -> bool:
        """Boolean indicating whether the system controlled by the
        thermostat has a fan. For simulation purposes this is
        always true.

        Returns:
            bool: Always true.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "has_fan"))
        return self._has_fan

    def set_has_fan(self, value: bool = True):
        """Setter for has_fan property.

        Args:
            value (bool, optional): The value to set has_fan to.
            Defaults to True.
        """
        self._logger.info(log_message_formatter(
            "set", f"{self}", "has_fan", value))
        self._has_fan = value

    @property
    def has_leaf(self) -> bool:
        """Boolean indicating whether the device is set to
        energy-saving temperature.

        Returns:
            bool: Whether thermostat is in energy saving mode.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "has_leaf"))
        return self._hvac_mode == "eco"

    @property
    def humidity(self) -> int:
        """Returns the humidity measured by the thermostat as a
        percentage between 0 and 100.

        Returns:
            int: Percentage humidity, between 0 and 100 inclusive.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "humidity"))
        return round(self._humidity * 100)

    @property
    def hvac_mode(self) -> str:
        """Getter for the current HVAC mode.

        Returns:
            str: The current HVAC mode.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "hvac_mode"))
        return self._hvac_mode

    def set_hvac_mode(self, value: str = "off"):
        """Setter for the HVAC mode.

        Args:
            value (str, optional): The value to set HVAC mode to. Must
            be "cool", "heat", "heat-cool", or "off". Defaults to "off".
        """
        if value in self._hvac_modes:
            self.set_previous_hvac_mode(self._hvac_mode)
            self._logger.info(log_message_formatter(
                "set", f"{self}", "hvac_mode", value))
            self._hvac_mode = value
        else:
            self._logger.warning(
                "abort set -- {value} not in {self._hvac_modes}")

    @property
    def is_cooling(self) -> bool:
        """Boolean indicating whether the system is actively cooling.

        Returns:
            bool: True if current temperature is greater than target
            temperature.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "is_cooling"))
        return (self._ambient_temperature > self._target_temperature) \
            and self.can_cool \
            and (self._hvac_mode == "cool" or self._hvac_mode == "heat-cool")

    @property
    def is_heating(self) -> bool:
        """Boolean indicating whether the system is actively heating.

        Returns:
            bool: True if current temperature is less than target
            temperature.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "is_heating"))
        return (self._ambient_temperature < self._target_temperature) \
            and self.can_heat \
            and (self._hvac_mode == "heat" or self._hvac_mode == "heat-cool")

    @property
    def is_locked(self) -> bool:
        """Getter for locked status of the device.

        Returns:
            bool: Whether the device is locked.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "is_locked"))
        return self._is_locked

    def set_is_locked(self, value: bool = False):
        """Setter for is_locked.

        Args:
            value (bool, optional): The desired lock status of the
            device. Defaults to False.
        """
        self._logger.info(log_message_formatter(
            "set", f"{self}", "is_locked", value))
        self._is_locked = value

    @property
    def is_using_emergency_heat(self) -> bool:
        """Boolean indicating whether the system controlled by the
        themostat is using emergency heat.

        Returns:
            bool: Whether the emergency heat is active.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "is_using_emergency_heat"))
        return False

    @property
    def label(self) -> str:
        """Getter method for user-settable device label.

        Returns:
            str: The device label.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "label"))
        return self._name

    def set_label(self, value: str = "nowhere"):
        """Setter for device label.

        Args:
            value (str, optional): The value to set the label to.
            Defaults to "nowhere".
        """
        self._logger.info(log_message_formatter(
            "set", f"{self}", "label"))
        self._name = value

    @property
    def locale(self) -> str:
        """Getter for locale.

        Returns:
            str: The current locale being used by the device.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "locale"))
        return self._locale

    @property
    def locked_temp_max_c(self) -> float:
        """Getter for locked max temperature, in Celsius.

        Returns:
            float: The locked maximum temperature, in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "locked_temp_max_c"))
        return kelvin_to_celsius(self._locked_temp_max)

    @property
    def locked_temp_max_f(self) -> float:
        """Getter for locked max temperature, in Fahrenheit.

        Returns:
            float: The locked maximum temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "locked_temp_max_f"))
        return celsius_to_fahrenheit(self.locked_temp_max_c)

    @property
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

        self._logger.debug(log_message_formatter(
            "get", f"{self}", "locked_temp_max"))

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

        self._logger.info(log_message_formatter(
            "set", f"{self}", "locked_temp_max", value))

    @property
    def locked_temp_min_c(self) -> float:
        """Getter for locked min temperature, in Celsius.

        Returns:
            float: The locked minimum temperature, in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "locked_temp_min_c"))
        return kelvin_to_celsius(self._locked_temp_min)

    @property
    def locked_temp_min_f(self) -> float:
        """Getter for locked min temperature, in Fahrenheit.

        Returns:
            float: The locked minimum temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "locked_temp_min_f"))
        return celsius_to_fahrenheit(self.locked_temp_min_c)

    @property
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

        self._logger.debug(log_message_formatter(
            "get", f"{self}", "locked_temp_min"))

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

        self._logger.info(log_message_formatter(
            "set", f"{self}", "locked_temp_min", value))

    @property
    def previous_hvac_mode(self) -> str:
        """Getter for previous HVAC mode.

        Returns:
            str: The HVAC mode previous to the current.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "previous_hvac_mode"))
        return self._previous_hvac_mode

    def set_previous_hvac_mode(self, value: str):
        """Setter for previous hvac mode.

        Args:
            value(str): The value to set previous hvac mode to.
        """

        if value in self._hvac_modes:
            self._logger.info(log_message_formatter(
                "set", f"{self}", "locked_temp_max_f", value))
            self._previous_hvac_mode = value
        else:
            self._logger.warning(
                "abort set -- {value} not in {self._hvac_modes}")

    @property
    def sunlight_correction_enabled(self) -> bool:
        """Getter for sunlight correction enabled.

        Returns:
            bool: Whether sunlight correction is enabled.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "sunlight_correction_enabled"))
        return self._sunlight_correction_enabled

    def set_sunlight_correction_enabled(self, value: bool = False):
        """Setter for sunlight correction enable.

        Args:
            value (bool, optional): The value to set sunlight correction
            to. Defaults to False.
        """
        self._logger.info(log_message_formatter(
            "set", f"{self}", "sunlight_correction_enabled", value))
        self._sunlight_correction_enabled = value

    @property
    def sunlight_correction_active(self) -> bool:
        """Getter for sunlight correction active.

        Returns:
            bool: Whether the sunlight correction is active.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "sunlight_correction_active"))
        return self._sunlight_correction_active

    def set_sunlight_correction_active(self, value: bool = False):
        """Setter for sunlight correction active status.

        Args:
            value (bool, optional): Value to set sunlight correction
            status to. Defaults to False.
        """
        self._logger.info(log_message_formatter(
            "set", f"{self}", "sunlight_correction_active", value))
        self._sunlight_correction_active = value

    @property
    def target_temperature(self) -> int:
        """Selects the appropriate target temperature based on HVAC mode
        and temperature scale.

        Returns:
            int: The target temperature in units specified by
            temperature scale.
        """
        # TODO: Find a better way to do this. This is ugly.
        if self._hvac_mode == "cool":
            return self.target_temperature_low
        elif self._hvac_mode == "heat":
            return self.target_temperature_high
        elif self._hvac_mode == "heat-cool":
            # TODO: Fix this so that heat or cool is chosen.
            if self._ambient_temperature >= self._target_temperature:
                return self.target_temperature_low
            elif self._ambient_temperature <= self._target_temperature:
                return self.target_temperature_high
        elif self._hvac_mode == "eco":
            if self._ambient_temperature >= self._target_temperature:
                return self.eco_temperature_low
            elif self._ambient_temperature <= self._target_temperature:
                return self.eco_temperature_high
        elif self._hvac_mode == "off":
            return self.ambient_temperature

        self._logger.debug(log_message_formatter(
            "get", f"{self}", "ambient_temperature"))

    @property
    def target_temperature_f(self) -> float:
        """Getter for target temperature.

        Returns:
            float: The target temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperature_f"))
        return celsius_to_fahrenheit(self.target_temperature_c)

    @property
    def target_temperature_c(self) -> float:
        """Getter for target temperature, in Celsius.

        Returns:
            float: The target temperature, in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperature_c"))
        return kelvin_to_celsius(self._target_temperature)

    @property
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

        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperature_high"))

    @property
    def target_temperature_high_f(self) -> float:
        """Getter for the target high temperature, in Fahrenheit.

        Returns:
            float: The target high temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperatue_high_f"))
        return celsius_to_fahrenheit(self.target_temperature_high_c)

    @property
    def target_temperature_high_c(self) -> float:
        """Getter for the target high temperature, in Celsius.

        Returns:
            float: The target high temperature, in Celsius.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperature_high_c"))
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

        self._logger.info(log_message_formatter(
            "set", f"{self}", "target_temperature_high", value))

    @property
    def target_temperature_low_f(self) -> float:
        """Getter for the target low temperature, in Fahrenheit.

        Returns:
            float: The target low temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperature_low_f"))
        return celsius_to_fahrenheit(self.target_temperature_low_c)

    @property
    def target_temperature_low_c(self) -> float:
        """Getter for the target low temperature, in Fahrenheit.

        Returns:
            float: The target low temperature, in Fahrenheit.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperature_low_c"))
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

        self._logger.info(log_message_formatter(
            "set", f"{self}", "target_temperature_low", value))

    @property
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

        self._logger.debug(log_message_formatter(
            "get", f"{self}", "target_temperature_low"))

    @property
    def temperature_scale(self) -> str:
        """Getter method for units.

        Returns:
            str: Current temperature units returned by the device.
        """
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "temperature_scale"))
        return self._temperature_scale

    def set_temperature_scale(self, scale: str = "K"):
        """Setter for units.

        Args:
            scale (str, optional): The target units. Must be "K", "C",
            or "F". Defaults to "K".
        """
        if scale in self._temperature_scales:
            self._logger.info(log_message_formatter(
                "set", f"{self}", "temperature_scale", scale))
            self._temperature_scale = scale
        else:
            self._logger.warning(
                "abort set -- {scale} not in {self._temperature_scales}")

    @property
    def time_to_target(self) -> str:
        """Calculates the time, in minutes, for the structure to reach
        the target temperature.

        Returns:
            str: A string representation of the estimated time.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "time_to_target"))
        return self._time_to_target_options[0]

    @property
    def time_to_target_training(self) -> str:
        """Getter for the time-to-temperature training mode.

        Returns:
            str: The training mode.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(log_message_formatter(
            "get", f"{self}", "time_to_target_training"))
        return self._training_modes[0]
