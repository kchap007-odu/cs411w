import unittest
import json
import os

from hamcrest import assert_that, close_to, contains_string, equal_to, is_,\
    is_not, string_contains_in_order

from devices import Thermostat


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

    def test_constructor(self):
        """Tests the constructor for NestThermostat class. Covers
        default constructor and constructor with arguments.
        """
        t = Thermostat.NestThermostat()
        assert_that(t.name_long, string_contains_in_order(
            "none", "Thermostat", "none"))

        t = Thermostat.NestThermostat(name="Nest", location="Living Room")
        assert_that(t.name_long, string_contains_in_order(
            "Nest", "Thermostat", "Living Room"))

    def test_multiple_instances(self):
        """Tests whether instance variables are unique to instances.
        """
        instance_one = Thermostat.NestThermostat()
        instance_two = Thermostat.NestThermostat()

        instance_one.set_is_locked(False)
        assert_that(instance_one.is_locked, is_(False))
        instance_two.set_is_locked(True)

        assert_that(instance_two.is_locked, is_(True))
        assert_that(instance_one.is_locked, is_(False))
        assert_that(instance_one.is_locked, is_not(instance_two.is_locked))

    def test__from_json__(self):
        t = Thermostat.NestThermostat()

        for scale in t._temperature_scales:
            params = {"temperature_scale": scale}
            t.__from_json__(params)
            assert_that(t.temperature_scale, is_(equal_to(scale)))

        for hvac_mode in t._hvac_modes:
            params = {"hvac_mode": hvac_mode}
            t.__from_json__(params)
            assert_that(t.hvac_mode, is_(equal_to(hvac_mode)))

        # ------------ Write the file as a part of the test ------------
        file = os.path.join(
            os.path.dirname(__file__), "test-thermostat-properties.json")

        with open(file, "w") as f:
            f.write(json.dumps(self._json_file_parameters, indent=4))
        # ---------------------- End file write ------------------------

        with open(file, "r") as f:
            dictionary = json.loads(f.read())

        t.__from_json__(dictionary)
        for k, v in dictionary.items():
            value = eval(f"t.{k}")
            if isinstance(v, int):
                assert_that(value, is_(close_to(v, self._tolerance)))
            else:
                assert_that(eval(f"t.{k}"), is_(equal_to(v)))

    def test_set_eco_temperature_high(self):
        t = Thermostat.NestThermostat()

        for scale, value in zip(self._scales, self._values):
            t.set_temperature_scale(scale)
            t.set_eco_temperature_high(value)
            assert_that(t.eco_temperature_high,
                        is_(close_to(value, self._tolerance)))

    def test_set_eco_temperature_low(self):
        t = Thermostat.NestThermostat()

        for scale, value in zip(self._scales, self._values):
            t.set_temperature_scale(scale)
            t.set_eco_temperature_low(value)
            assert_that(t.eco_temperature_low,
                        is_(close_to(value, self._tolerance)))

    def test_set_fan_timer_duration(self):
        """Tests the ability to set the fan timer duration.
        """
        t = Thermostat.NestThermostat()

        for duration in self._durations:
            t.set_fan_timer_duration(minutes=duration)
            assert_that(t.fan_timer_duration, is_(duration))

    def test_set_has_fan(self):
        t = Thermostat.NestThermostat()

        for value in self._boolean_values:
            t.set_has_fan(value)
            assert_that(t.has_fan, is_(value))

    def test_set_hvac_mode(self):
        t = Thermostat.NestThermostat()
        previous = t.hvac_mode

        for mode in t._hvac_modes:
            t.set_hvac_mode(value=mode)
            assert_that(t.hvac_mode, is_(mode))
            assert_that(t.previous_hvac_mode, is_(previous))
            # All temperatures should default to zero.
            assert_that(t.target_temperature, is_(equal_to(0)))
            assert_that(t.has_leaf, is_(equal_to(mode == "eco")))
            previous = t.hvac_mode

    def test_set_is_locked(self):
        t = Thermostat.NestThermostat()

        for locked in self._boolean_values:
            t.set_is_locked(locked)
            assert_that(t.is_locked, is_(locked))

    def test_set_label(self):
        t = Thermostat.NestThermostat()

        for label in self._labels:
            t.set_label(label)
            assert_that(t.label, is_(equal_to(label)))
            assert_that(t.name_long, contains_string(label))

    def test_set_locked_temp_max(self):
        t = Thermostat.NestThermostat()

        for scale, value in zip(self._scales, self._values):
            t.set_temperature_scale(scale)
            t.set_locked_temp_max(value)
            assert_that(t.locked_temp_max,
                        is_(close_to(value, self._tolerance)))

    def test_set_locked_temp_min(self):
        t = Thermostat.NestThermostat()

        for scale, value in zip(self._scales, self._values):
            t.set_temperature_scale(scale)
            t.set_locked_temp_min(value)
            assert_that(t.locked_temp_min,
                        is_(close_to(value, self._tolerance)))

    def test_set_previous_hvac_mode(self):
        t = Thermostat.NestThermostat()

        for value in t._hvac_modes:
            t.set_previous_hvac_mode(value)
            assert_that(t.previous_hvac_mode, is_(equal_to(value)))

    def test_set_sunlight_correction_active(self):
        t = Thermostat.NestThermostat()

        for value in self._boolean_values:
            t.set_sunlight_correction_active(value)
            assert_that(t.sunlight_correction_active, is_(equal_to(value)))

    def test_set_sunlight_correction_enabled(self):
        t = Thermostat.NestThermostat()

        for value in self._boolean_values:
            t.set_sunlight_correction_enabled(value)
            assert_that(t.sunlight_correction_enabled, is_(equal_to(value)))

    def test_set_target_temperature_high(self):
        t = Thermostat.NestThermostat()

        for scale, value in zip(self._scales, self._values):
            t.set_temperature_scale(scale)
            t.set_target_temperature_high(value)
            assert_that(t.target_temperature_high,
                        is_(close_to(value, self._tolerance)))

    def test_set_target_temperature_low(self):
        t = Thermostat.NestThermostat()

        for scale, value in zip(self._scales, self._values):
            t.set_temperature_scale(scale)
            t.set_eco_temperature_low(value)
            assert_that(t.eco_temperature_low,
                        is_(close_to(value, self._tolerance)))

    def test_set_temperature_scale(self):
        """Tests the ability to change the temperature scale of the
        device.
        """
        t = Thermostat.NestThermostat()

        for scale in t._temperature_scales:
            t.set_temperature_scale(scale)
            assert_that(t.temperature_scale, is_(equal_to(scale)))


if __name__ == "__main__":
    unittest.main()
