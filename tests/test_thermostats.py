import unittest
import json
import os

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL  # noqa F401

from hamcrest import assert_that, close_to, contains_string, equal_to, is_,\
    is_not, string_contains_in_order

from devices.thermostats import NestThermostat
from helpers.misc import create_logger


class TestNestThermostat(unittest.TestCase):
    _scales = ["F", "C", "K"]
    _values = [90, 30, 200]
    _durations = [10, 60]
    _tolerance = 0.1
    _labels = ["Test", "New", "Third", "testing123"]
    _boolean_values = [True, False]
    _json_file_parameters = {
        "device_type": "Thermostat",
        "hvac_mode": "cool",
        "previous_hvac_mode": "off",
        "locked_temp_max": 75,
        "locked_temp_min": 71,
        "target_temperature_high": 75,
        "target_temperature_low": 70,
        "eco_temperature_high": 76,
        "eco_temperature_low": 74,
        "temperature_scale": "F",
        "has_fan": True,
        "is_locked": False,
        "fan_timer_duration": 5,
        "name": "Nest",
        "location": "Upstairs",
        "device_id": "1234",
        "sunlight_correction_active": False,
        "sunlight_correction_enabled": False
    }

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join(os.path.dirname(__file__),
                               "logs", "test-thermostats.log")
        cls._logger = create_logger(
            filename=logfile, file_log_level=DEBUG,
            standard_out_log_level=CRITICAL)

    def setUp(self):
        self.default_constructor = NestThermostat(logger=self._logger)
        self.instance_two = NestThermostat(logger=self._logger)
        self.non_default_constructor = NestThermostat(
            name="Nest", location="Living Room", logger=self._logger)

    def test_constructor(self):
        """Tests the constructor for NestThermostat class. Covers
        default constructor and constructor with arguments.
        """
        assert_that(self.default_constructor.name_long,
                    string_contains_in_order("none", "Thermostat", "none"))

        assert_that(self.non_default_constructor.name_long,
                    string_contains_in_order(
                        "Nest", "Thermostat", "Living Room"))

    def test_multiple_instances(self):
        """Tests whether instance variables are unique to instances.
        """

        self.default_constructor.set_is_locked(False)
        assert_that(self.default_constructor.is_locked, is_(False))
        self.instance_two.set_is_locked(True)

        assert_that(self.instance_two.is_locked, is_(True))
        assert_that(self.default_constructor.is_locked, is_(False))
        assert_that(self.default_constructor.is_locked,
                    is_not(self.instance_two.is_locked))

    def test__from_json__(self):
        for scale in self.default_constructor._temperature_scales:
            params = {"temperature_scale": scale}
            self.default_constructor.__from_json__(params)
            assert_that(self.default_constructor.temperature_scale,
                        is_(equal_to(scale)))

        for hvac_mode in self.default_constructor._hvac_modes:
            params = {"hvac_mode": hvac_mode}
            self.default_constructor.__from_json__(params)
            assert_that(self.default_constructor.hvac_mode,
                        is_(equal_to(hvac_mode)))

        # ------------ Write the file as a part of the test ------------
        file = os.path.join(
            os.path.dirname(__file__), "test-thermostat-properties.json")

        with open(file, "w") as f:
            f.write(json.dumps(self._json_file_parameters, indent=4))
        # ---------------------- End file write ------------------------

        with open(file, "r") as f:
            dictionary = json.loads(f.read())

        self.default_constructor.__from_json__(dictionary)
        for k, v in dictionary.items():
            value = eval(f"self.default_constructor.{k}")
            if isinstance(v, int):
                assert_that(value, is_(close_to(v, self._tolerance)))
            else:
                assert_that(
                    eval(f"self.default_constructor.{k}"), is_(equal_to(v)))

    def test_set_eco_temperature_high(self):
        for scale, value in zip(self._scales, self._values):
            self.default_constructor.set_temperature_scale(scale)
            self.default_constructor.set_eco_temperature_high(value)
            assert_that(self.default_constructor.eco_temperature_high,
                        is_(close_to(value, self._tolerance)))

    def test_set_eco_temperature_low(self):
        for scale, value in zip(self._scales, self._values):
            self.default_constructor.set_temperature_scale(scale)
            self.default_constructor.set_eco_temperature_low(value)
            assert_that(self.default_constructor.eco_temperature_low,
                        is_(close_to(value, self._tolerance)))

    def test_set_fan_timer_duration(self):
        """Tests the ability to set the fan timer duration.
        """
        for duration in self._durations:
            self.default_constructor.set_fan_timer_duration(minutes=duration)
            assert_that(self.default_constructor.fan_timer_duration,
                        is_(duration))

    def test_set_has_fan(self):
        """Tests ability to set whether system has fan.
        """
        for value in self._boolean_values:
            self.default_constructor.set_has_fan(value)
            assert_that(self.default_constructor.has_fan, is_(value))

    def test_set_hvac_mode(self):
        """Tests ability to set hvac mode.
        """
        previous = self.default_constructor.hvac_mode

        for mode in self.default_constructor._hvac_modes:
            self.default_constructor.set_hvac_mode(value=mode)
            assert_that(self.default_constructor.hvac_mode, is_(mode))
            assert_that(self.default_constructor.previous_hvac_mode,
                        is_(previous))
            # All temperatures should default to zero.
            assert_that(self.default_constructor.target_temperature,
                        is_(equal_to(0)))
            assert_that(self.default_constructor.has_leaf,
                        is_(equal_to(mode == "eco")))
            previous = self.default_constructor.hvac_mode

    def test_set_is_locked(self):
        for locked in self._boolean_values:
            self.default_constructor.set_is_locked(locked)
            assert_that(self.default_constructor.is_locked, is_(locked))

    def test_set_label(self):
        for label in self._labels:
            self.default_constructor.set_label(label)
            assert_that(self.default_constructor.label, is_(equal_to(label)))
            assert_that(self.default_constructor.name_long,
                        contains_string(label))

    def test_set_locked_temp_max(self):
        for scale, value in zip(self._scales, self._values):
            self.default_constructor.set_temperature_scale(scale)
            self.default_constructor.set_locked_temp_max(value)
            assert_that(self.default_constructor.locked_temp_max,
                        is_(close_to(value, self._tolerance)))

    def test_set_locked_temp_min(self):
        for scale, value in zip(self._scales, self._values):
            self.default_constructor.set_temperature_scale(scale)
            self.default_constructor.set_locked_temp_min(value)
            assert_that(self.default_constructor.locked_temp_min,
                        is_(close_to(value, self._tolerance)))

    def test_set_previous_hvac_mode(self):
        for value in self.default_constructor._hvac_modes:
            self.default_constructor.set_previous_hvac_mode(value)
            assert_that(self.default_constructor.previous_hvac_mode,
                        is_(equal_to(value)))

    def test_set_sunlight_correction_active(self):
        for value in self._boolean_values:
            self.default_constructor.set_sunlight_correction_active(value)
            assert_that(
                self.default_constructor.sunlight_correction_active,
                is_(equal_to(value)))

    def test_set_sunlight_correction_enabled(self):
        for value in self._boolean_values:
            self.default_constructor.set_sunlight_correction_enabled(value)
            assert_that(
                self.default_constructor.sunlight_correction_enabled,
                is_(equal_to(value)))

    def test_set_target_temperature_high(self):
        for scale, value in zip(self._scales, self._values):
            self.default_constructor.set_temperature_scale(scale)
            self.default_constructor.set_target_temperature_high(value)
            assert_that(self.default_constructor.target_temperature_high,
                        is_(close_to(value, self._tolerance)))

    def test_set_target_temperature_low(self):
        for scale, value in zip(self._scales, self._values):
            self.default_constructor.set_temperature_scale(scale)
            self.default_constructor.set_eco_temperature_low(value)
            assert_that(self.default_constructor.eco_temperature_low,
                        is_(close_to(value, self._tolerance)))

    def test_set_temperature_scale(self):
        """Tests the ability to change the temperature scale of the
        device.
        """
        for scale in self.default_constructor._temperature_scales:
            self.default_constructor.set_temperature_scale(scale)
            assert_that(self.default_constructor.temperature_scale,
                        is_(equal_to(scale)))


if __name__ == "__main__":
    unittest.main()
