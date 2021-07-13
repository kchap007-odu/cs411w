import datetime

import Devices


TEMPERATURE_SCALES = ["K", "C", "F"]
HVAC_MODES = ["heat", "cool", "heat-cool", "eco", "off"]
TIMES_TO_TARGET = ["~0", "<5", "~15", "~90", "120"]
TRAINING = ["training", "ready"]
DEGREES_PER_MINUTE = 1


class NestThermostat(Devices.SmartDevice):
    """
    A smart thermostat class based on the Nest API.

    https://developers.nest.com/reference/api-thermostat
    """
    # All temperature units should be stored in Kelvin.
    _ambient_temperature: int = 293
    _eco_temperature_low: int = 297
    _eco_temperature_high: int = 299
    _fan_timer_duration: datetime.datetime = None
    _has_fan: bool = True
    _humidity: float = 0.5
    _hvac_mode: str = "off"
    _is_locked: bool = False
    _locale: str = "NOT IMPLEMENTED"
    _locked_temp_min: int = 293
    _locked_temp_max: int = 300
    _previous_hvac_mode: str = ""
    _structure_id: str = "NOT IMPLEMENTED"
    _sunlight_correction_enabled: bool = False
    _sunlight_correction_active: bool = False
    # All temperature units should be stored in Kelvin.
    _target_temperature: int = 273
    _target_temperature_high: int = 303
    _target_temperature_low: int = 293
    _temperature_scale: str = "C"
    _where_id: str = "NOT YET IMPLEMENTED"
    _where_name: str = "NOT YET IMPLEMENTED"

    def __init__(self, location: str = "none"):
        super().__init__()
        self._device_type = "Thermostat"
        self._logger.debug(
            f"Device {self._device_id} is now a {self._device_type}."
        )

    @property
    def ambient_temperature(self) -> int:
        """
        Getter method for ambient temperature.

        Return:
        int: The current temperature as measured at the device, in
        Kelvin.
        """
        self._logger.debug(
            f"Get value of temperature for device {self._device_id}\
                in units {self._temperature_scale}."
        )
        if self.temperature_scale == "F":
            return self.ambient_temperature_f
        elif self.temperature_scale == "C":
            return self.ambient_temperature_c
        else:
            return self._ambient_temperature

    @property
    def ambient_temperature_c(self) -> int:
        """
        Getter for ambient temperature.

        Returns:
        int: The ambient temperature, as measured at the device, in
        Celsius.
        """
        self._logger.debug(
            f"Get ambient temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._ambient_temperature)

    @property
    def ambient_temperature_f(self) -> int:
        """
        Getter for ambient temperature in Fahrenheit.

        Returns:
        int: The ambient temperature, as measured at the device, in
        Celsius.
        """
        self._logger.debug(
            f"Get ambient temperature (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.ambient_temperature_c)

    def as_dict(self) -> dict:
        """
        Representation of the object state as a dictionary.

        Returns:
        dict: The internal state of the device."""
        self._logger.debug(f"Get device {self._device_id} as dictionary.")
        return {
            "device_id": self.device_id,
            "status": self._status,
            "humidity": self.humidity,
            "temperature": self.ambient_temperature,
            "temperature_scale": self.temperature_scale,
            "hvac_mode": self.hvac_mode
        }

    @property
    def can_heat(self) -> bool:
        """
        Boolean indicating whether the system controlled by the
        thermostat is capable of heating. For simulation purposes
        this is always true.

        Returns
        bool: Always true.
        """
        self._logger.debug(
            f"Get heating capability for device {self._device_id}."
        )
        return True

    @property
    def can_cool(self) -> bool:
        """
        Boolean indicating whether the system controlled by the
        thermostat is capable of cooling. For simulation purposes
        this is always true.

        Returns
        bool: Always true.
        """
        self._logger.debug(
            f"Get cooling capability for device {self._device_id}."
        )
        return True

    @property
    def eco_temperature_high_f(self) -> int:
        """
        Getter for the target high temperature, in Fahrenheit.

        Returns:
        int: The high eco temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get high eco temperature (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.eco_temperature_high_c)

    def set_eco_temperature_high(self, value: int = 0):
        """
        Setter for high eco temperature value. Assumes set units are
        the same as the current system units.

        Parameters:
        value (int): The temperature to set the high eco value to.
        """
        if self._temperature_scale == "F":
            self._eco_temperature_high = celsius_to_kelvin(
                fahrenheit_to_celsius(value)
            )
        elif self._temperature_scale == "C":
            self._eco_temperature_high = celsius_to_kelvin(value)

    @property
    def eco_temperature_low_f(self) -> int:
        """
        Getter for the target low eco temperature, in Fahrenheit.

        Returns:
        int: The low eco temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get low eco temperature (F) for device {self._device_id}"
        )
        return celsius_to_fahrenheit(self.eco_temperature_low_c)

    @property
    def eco_temperature_high_c(self) -> int:
        """
        Getter for the target high eco temperature, in Celsius.

        Returns:
        int: The high eco temperature, in Celsius.
        """
        self._logger.debug(
            f"Get high eco temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._eco_temperature_high)

    @property
    def eco_temperature_low_c(self) -> int:
        """
        Getter for the target low eco temperature, in Celsius.

        Returns:
        int: The high eco temperature, in Celsius.
        """
        self._logger.debug(
            f"Get low eco temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._eco_temperature_low)

    @property
    def fan_timer_active(self) -> bool:
        """
        Boolean indicating whether the fan timer is active.

        Returns
        bool: True if fan timer is active, false otherwise.
        """
        self._logger.debug(
            f"Get fan timer active status for device {self._device_id}."
        )
        return self.fan_timer_timeout > datetime.datetime.now()

    @property
    def fan_timer_timeout(self) -> datetime.datetime:
        """
        The time at which the fan timer will reach zero.

        Returns:
        datetime.datetime: The time at which the fan will become
        inactive.
        """
        self._logger.debug(
            f"Get fan timer timeout for device {self._device_id}."
        )
        return datetime.datetime.now() + self.fan_timer_duration

    @property
    def fan_timer_duration(self) -> datetime.datetime:
        """
        Getter for fan timer duration.

        Returns:
        datetime.datetime: The fan timer duration.
        """
        self._logging.debug(
            f"Get fan timer duration for device {self._device_id}."
        )
        return self._fan_timer_duration

    def set_fan_timer_duration(self, value: int = 5):
        """
        Setter for fan timer duration.

        Parameters:
        value (int): The duration, in minutes, to set the fan timer.
        """
        self._fan_timer_duration = datetime.datetime(minute=value)
        self._logger.debug(
            f"Set timeout for device {self._device_id} to \
                {value} mintues (datetime value {self._fan_timer_duration}."
        )

    @property
    def has_fan(self) -> bool:
        """
        Boolean indicating whether the system controlled by the
        thermostat has a fan. For simulation purposes this is
        always true.

        Returns
        bool: Always true.
        """
        self._logger.debug(f"Get fan status for device {self._device_id}.")
        return True

    @property
    def has_leaf(self) -> bool:
        """
        Boolean indicating whether the device is set to
        energy-saving temperature.

        Returns:
        bool: Whether thermostat is in energy saving mode.
        """
        self._logger.debug(f"Get leaf status for device {self._device_id}.")
        return self._hvac_mode == "eco"

    @property
    def humidity(self) -> float:
        """
        Returns the humidity measured by the thermostat as a percentage
        between 0 and 1.

        Returns:
        float: Percentage humidity, between 0 and 1 inclusive.
        """
        self._logger.debug(
            f"Get value of humidity for device {self._device_id}."
        )
        return self._humidity

    @property
    def hvac_mode(self) -> str:
        """
        Getter for the current HVAC mode.

        Returns:
        str: The current HVAC mode.
        """
        self._logger.debug(f"Get HVAC mode for device {self._device_id}.")
        return self._hvac_mode

    def set_hvac_mode(self, value: str = "off"):
        """
        Setter for the HVAC mode.

        Parameters:
        value (str): The value to set HVAC mode to. Must be "cool",
        "heat", "heat-cool", or "off".
        """
        if value in HVAC_MODES:
            self._logger.debug(
                f"Set previous HVAC value of device {self._device_id} \
                    to {self._hvac_mode}"
            )
            self._previous_hvac_mode = self._hvac_mode
            self._logger.debug(
                f"Set HVAC mode of device {self._device_id} to {value}."
            )
            self._hvac_mode = value

    @property
    def is_cooling(self) -> bool:
        """
        Boolean indicating whether the system is actively cooling.

        Returns
        bool: True if current temperature is greater than target
        temperature.
        """
        # TODO: Need to add logic for whether device is set to cool.
        self._logger.debug(f"Get cooling status of device {self._device_id}.")
        return (self._ambient_temperature > self._target_temperature) \
            and self.can_cool \
            and (self._hvac_mode == "cool" or self._hvac_mode == "heat-cool")

    @property
    def is_heating(self) -> bool:
        """
        Boolean indicating whether the system is actively heating.

        Returns
        bool: True if current temperature is less than target
        temperature.
        """
        # TODO: Need to add logic for whether device is set to heat.
        self._logger.debug(f"Get heating status of device {self._device_id}.")
        return (self._ambient_temperature < self._target_temperature) \
            and self.can_heat \
            and (self._hvac_mode == "heat" or self._hvac_mode == "heat-cool")

    @property
    def is_locked(self) -> bool:
        """
        Getter for locked status of the device.

        Returns:
        bool: Whether the device is locked.
        """
        self._logger.debug(f"Get locked status of device {self._device_id}")
        return self._is_locked

    @property
    def set_is_locked(self, value: bool = False):
        """
        Setter for is_locked.

        Parameters:
        value (bool): The desired lock status of the device.
        """
        self._is_locked = value
        self._logger.debug(
            f"Set locked status of device {self._device_id} to {value}."
        )

    @property
    def is_using_emergency_heat(self) -> bool:
        """
        Boolean indicating whether the system controlled by the
        themostat is using emergency heat.

        Returns:
        bool: Whether the emergency heat is active.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(
            f"Get emergency heat status of device {self._device_id}"
        )
        return False

    @property
    def label(self) -> str:
        """
        Getter method for user-settable device label.

        Returns:
        str: The device label.
        """
        self._logger.debug(f"Get label for device {self._device_id}.")
        return self._label

    def set_label(self, value: str = "nowhere"):
        """
        Setter for device label.

        Parameters:
        value (str): The value to set the label to.
        """
        self._logger.debug(
            f"Set value of label for device {self._device_id} to {value}."
        )
        self._label = value

    @property
    def locale(self) -> str:
        """
        Getter for locale.

        Returns:
        str: The current locale being used by the device.
        """
        self._logger.debug(
            f"Get value of locale for device {self._device_id}."
        )
        return self._locale

    @property
    def locked_temp_max_c(self) -> int:
        """
        Getter for locked max temperature, in Celsius.

        Returns:
        int: The locked maximum temperature, in Celsius.
        """
        self._logger.debug(
            f"Get locked temp (C) max status for device {self._device_id}."
        )
        return kelvin_to_celsius(self._locked_temp_max)

    @property
    def locked_temp_min_c(self) -> int:
        """
        Getter for locked min temperature, in Celsius.

        Returns:
        int: The locked minimum temperature, in Celsius.
        """
        self._logger.debug(
            f"Get locked temp (C) min status for device {self._device_id}."
        )
        return kelvin_to_celsius(self._locked_temp_min)

    @property
    def locked_temp_max_f(self) -> int:
        """
        Getter for locked max temperature, in Fahrenheit.

        Returns:
        int: The locked maximum temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get locked temp (F) max for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.locked_temp_max_c)

    @property
    def locked_temp_min_f(self) -> int:
        """
        Getter for locked min temperature, in Fahrenheit.

        Returns:
        int: The locked minimum temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get locked temp (F) min for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.locked_temp_min_c)

    @property
    def previous_hvac_mode(self) -> str:
        """
        Getter for previous HVAC mode.

        Returns:
        str: The HVAC mode previous to the current.
        """
        self._logger.debug(
            f"Get previous HVAC mode for device {self._device_id}."
        )
        return self._previous_hvac_mode

    @property
    def sunlight_correction_enabled(self) -> bool:
        """
        Getter for sunlight correction enabled.

        Returns:
        bool: Whether sunlight correction is enabled.
        """
        self._logger.debug(
            f"Get sunlight correction enable \
                status for device {self._device_id}."
        )
        return self._sunlight_correction_enabled

    @property
    def sunlight_correction_active(self) -> bool:
        """
        Getter for sunlight correction active.

        Returns:
        bool: Whether the sunlight correction is active.
        """
        self._logger.debug(
            f"Get sunlight correction active \
                status for device {self._device_id}."
        )
        return self._sunlight_correction_active

    @property
    def target_temperature(self) -> int:
        # TODO: Fill out this section.
        return None

    @property
    def target_temperature_f(self) -> int:
        """
        Getter for target temperature.

        Returns:
        int: The target temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.target_temperature_c)

    @property
    def target_temperature_c(self) -> int:
        """
        Getter for target temperature, in Celsius.

        Returns:
        int: The target temperature, in Celsius.
        """
        self._logger.debug(
            f"Get target temperature (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._target_temperature)

    @property
    def target_temperature_high_f(self) -> int:
        """
        Getter for the target high temperature, in Fahrenheit.

        Returns:
        int: The target high temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature high (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.target_temperature_high_c)

    @property
    def target_temperature_high_c(self) -> int:
        """
        Getter for the target high temperature, in Celsius.

        Returns:
        int: The target high temperature, in Celsius.
        """
        self._logger.debug(
            f"Get target temperature high (C) for device {self._device_id}."
        )
        return kelvin_to_celsius(self._target_temperature_high)

    @property
    def target_temperature_low_f(self) -> int:
        """
        Getter for the target low temperature, in Fahrenheit.

        Returns:
        int: The target low temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature low (F) for device {self._device_id}."
        )
        return celsius_to_fahrenheit(self.target_temperature_low_c)

    @property
    def target_temperature_low_c(self) -> int:
        """
        Getter for the target low temperature, in Fahrenheit.

        Returns:
        int: The target low temperature, in Fahrenheit.
        """
        self._logger.debug(
            f"Get target temperature low (C) for device {self._device_id}"
        )
        return kelvin_to_celsius(self._target_temperature_low)

    @property
    def temperature_scale(self) -> str:
        """
        Getter method for units.

        Returns:
        str: Current temperature units returned by the device.
        """
        self._logger.debug(f"Get value of units for device {self._device_id}.")
        return self._temperature_scale

    def set_temperature_scale(self, scale: str = "kelvin"):
        """
        Setter for units.

        Parameters:
        scale (str): The target units. Must be "K", "C", or "F"
        """
        if scale in TEMPERATURE_SCALES:
            self._logger.debug(
                f"Set value of scale for device {self._device_id} to {scale}."
            )
            self._temperature_scale = scale

    @property
    def time_to_target(self) -> str:
        """
        Calculates the time, in minutes, for the structure to reach
        the target temperature.

        Returns:
        str: A string representation of the estimated time.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(
            f"Get value of time to target for device {self._device_id}."
        )
        return TIMES_TO_TARGET[0]

    @property
    def time_to_target_training(self) -> str:
        """
        Getter for the time-to-temperature training mode.

        Returns:
        str: The training mode.
        """
        # TODO: Figure out how to implement this.
        self._logger.debug(
            f"Get value of time to target training \
                for device {self._device_id}."
        )
        return TRAINING[0]


def kelvin_to_celsius(value: int = 0) -> int:
    """
    Converts a value from Kelvin temperature scale to
    Celsius temperature scale.

    Parameters:
    value (int): The value to convert.

    Returns:
    int: The equivalent value in Celsius.
    """
    return int(value - 273.15)


def celsius_to_kelvin(value: int = 0) -> int:
    """
    Converts a value from Celsius temperature scale to Kelvin
    temperature scale.

    Parameters:
    value (int): The value to convert.

    Returns:
    int: The equivalent value in Kelvin.
    """
    return int(value + 273.15)


def celsius_to_fahrenheit(value: int = 0) -> int:
    """
    Converts a value from Celsius temperature scale to Fahrenheit
    temperature scale.

    Parameters:
    value (int): The value to convert.

    Returns:
    int: The equivalent value in Fahrenheit.
    """
    return int(value * (9/5) + 32)


def fahrenheit_to_celsius(value: int = 0) -> int:
    """
    Converts a value from Fahrenheit temperature scale to Celsius
    temperature scale.

    Parameters:
    value (int): The value to convert.

    Returns:
    int: The equivalent value in Celsius.
    """
    return (value - 32) * (5/9)


if __name__ == "__main__":
    thermo = NestThermostat(location="Upstairs")
    thermo.set_status("on")
    thermo.set_hvac_mode("cool")
    print(thermo.as_dict())
