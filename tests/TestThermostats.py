import unittest
import datetime
import json
import os

from hamcrest import assert_that, close_to, contains_string, equal_to, is_,\
    is_not, string_contains_in_order

from devices import Thermostat


TOLERANCE = 0.1


class TestThermostats(unittest.TestCase):
    def test_constructor(self):
        t = Thermostat.NestThermostat()
        assert_that(t.name_long, string_contains_in_order(
            "none", "Thermostat", "none"))

        t = Thermostat.NestThermostat(name="Nest", location="Living Room")
        assert_that(t.name_long, string_contains_in_order(
            "Nest", "Thermostat", "Living Room"))

    def test_multiple_instances(self):
        instance_one = Thermostat.NestThermostat()
        instance_two = Thermostat.NestThermostat()

        instance_one.set_is_locked(False)
        assert_that(instance_one.is_locked, is_(False))
        instance_two.set_is_locked(True)

        assert_that(instance_two.is_locked, is_(True))
        assert_that(instance_one.is_locked, is_(False))
        assert_that(instance_one.is_locked, is_not(instance_two.is_locked))

    def test_set_temperature_scale(self):
        t = Thermostat.NestThermostat()

        scales = Thermostat.TEMPERATURE_SCALES

        for scale in scales:
            t.set_temperature_scale(scale)
            assert_that(t.temperature_scale, is_(equal_to(scale)))

    def test_set_fan_timer_duration(self):
        t = Thermostat.NestThermostat()

        durations = [10, 60]

        for duration in durations:
            t.set_fan_timer_duration(minutes=duration)
            assert_that(t.fan_timer_duration, is_(
                equal_to(datetime.timedelta(minutes=duration))))

    def test_set_eco_temperature_high(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_eco_temperature_high(value=70)
        assert_that(t.eco_temperature_high_f, close_to(70, TOLERANCE))

        t.set_temperature_scale("C")
        t.set_eco_temperature_high(value=30)
        assert_that(t.eco_temperature_high_c, close_to(30, TOLERANCE))

        t.set_temperature_scale("K")
        t.set_eco_temperature_high(value=290)
        assert_that(t._eco_temperature_high, close_to(290, TOLERANCE))

    def test_set_eco_temperature_low(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_eco_temperature_low(value=70)
        assert_that(t.eco_temperature_low_f, close_to(70, TOLERANCE))

        t.set_temperature_scale("C")
        t.set_eco_temperature_low(value=30)
        assert_that(t.eco_temperature_low_c, close_to(30, TOLERANCE))

        t.set_temperature_scale("K")
        t.set_eco_temperature_low(value=290)
        assert_that(t._eco_temperature_low, close_to(290, TOLERANCE))

    def test_set_hvac_mode(self):
        t = Thermostat.NestThermostat()

        # Test default values. These may change.
        self.assertEqual(t.hvac_mode, "off")
        self.assertEqual(t.previous_hvac_mode, "")

        previous = t.hvac_mode

        modes = Thermostat.HVAC_MODES
        for mode in modes:
            t.set_hvac_mode(value=mode)
            assert_that(t.hvac_mode, is_(mode))
            assert_that(t.previous_hvac_mode, is_(previous))
            previous = t.hvac_mode

    def test_set_is_locked(self):
        t = Thermostat.NestThermostat()

        # Test the default value.
        assert_that(t.is_locked, is_(False))

        t.set_is_locked(value=True)
        assert_that(t.is_locked, is_(True))

        t.set_is_locked(value=False)
        assert_that(t.is_locked, is_(False))

    def test_set_locked_temp_max(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_locked_temp_max(value=90)
        assert_that(t.locked_temp_max_f, close_to(90, TOLERANCE))

        t.set_temperature_scale("C")
        t.set_locked_temp_max(value=30)
        assert_that(t.locked_temp_max_c, close_to(30, TOLERANCE))

        t.set_temperature_scale("K")
        t.set_locked_temp_max(value=290)
        assert_that(t._locked_temp_max, close_to(290, TOLERANCE))

    def test_set_locked_temp_min(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_locked_temp_min(value=60)
        assert_that(t.locked_temp_min_f, close_to(60, TOLERANCE))

        t.set_temperature_scale("C")
        t.set_locked_temp_min(value=10)
        assert_that(t.locked_temp_min_c, close_to(10, TOLERANCE))

        t.set_temperature_scale("K")
        t.set_locked_temp_min(value=260)
        assert_that(t._locked_temp_min, close_to(260, TOLERANCE))

    def test_set_target_temperature_high(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_target_temperature_high(value=90)
        assert_that(t.target_temperature_high_f, close_to(90, TOLERANCE))

        t.set_temperature_scale("C")
        t.set_target_temperature_high(value=30)
        assert_that(t.target_temperature_high_c, close_to(30, TOLERANCE))

        t.set_temperature_scale("K")
        t.set_target_temperature_high(value=290)
        assert_that(t._target_temperature_high, close_to(290, TOLERANCE))

    def test_set_target_temperature_low(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_target_temperature_low(value=60)
        assert_that(t.target_temperature_low_f, close_to(60, TOLERANCE))

        t.set_temperature_scale("C")
        t.set_target_temperature_low(value=10)
        assert_that(t.target_temperature_low_c, close_to(10, TOLERANCE))

        t.set_temperature_scale("K")
        t.set_target_temperature_low(value=260)
        assert_that(t._target_temperature_low, close_to(260, TOLERANCE))

    def test_set_from_json(self):
        t = Thermostat.NestThermostat()
        for scale in Thermostat.TEMPERATURE_SCALES:
            params = {"temperature_scale": scale}
            t._from_json(params)
            assert_that(t.temperature_scale, is_(equal_to(scale)))

        for hvac_mode in Thermostat.HVAC_MODES:
            params = {"hvac_mode": hvac_mode}
            t._from_json(params)
            assert_that(t.hvac_mode, is_(equal_to(hvac_mode)))

        parameters = {
            "temperature_scale": "F",
            "eco_temperature_high": 75,
            "eco_temperature_low": 70,
            "target_temperature_high": 75,
            "target_temperature_low": 70,
            "hvac_mode": "cool",
            "has_leaf": True,
            "is_locked": True,
            "name": "Nest",
            "location": "Upstairs",
            "device_id": "1234",
            "previous_hvac_mode": "off",
            "locked_temp_max": 75,
            "locked_temp_min": 71,
            "sunlight_correction_active": True,
            "sunlight_correction_enabled": True
        }
        file = os.path.join(
            os.path.dirname(__file__), "thermostat-properties.json")

        fid = open(file, "w")
        fid.write(json.dumps(parameters, indent=4))
        fid.close()

        # TODO: Add test for reading JSON from file.
        fid = open(file)
        dictionary = json.loads(fid.read())
        fid.close()

        t._from_json(dictionary)
        assert_that(t.temperature_scale, is_(equal_to("F")))
        assert_that(t.eco_temperature_high, is_(close_to(75, TOLERANCE)))
        assert_that(t.eco_temperature_low, is_(close_to(70, TOLERANCE)))
        assert_that(t.target_temperature_high, is_(close_to(75, TOLERANCE)))
        assert_that(t.target_temperature_low, is_(close_to(70, TOLERANCE)))
        assert_that(t.hvac_mode, is_(equal_to("cool")))
        assert_that(t.name, is_(equal_to("Nest")))
        assert_that(t.location, is_(equal_to("Upstairs")))
        assert_that(t.device_id, is_(equal_to("1234")))
        assert_that(t.previous_hvac_mode, is_(equal_to("off")))
        assert_that(t.locked_temp_max, is_(close_to(75, TOLERANCE)))
        assert_that(t.locked_temp_min, is_(close_to(71, TOLERANCE)))
        assert_that(t.sunlight_correction_active, is_(True))
        assert_that(t.sunlight_correction_enabled, is_(True))

    def test_set_label(self):
        t = Thermostat.NestThermostat()

        t.set_label("Test")
        assert_that(t.name_long, contains_string("Test"))

        t.set_label("New")
        assert_that(t.name_long, contains_string("New"))

    def test_fahrenheit_to_celsius(self):
        value = Thermostat.fahrenheit_to_celsius(32)
        assert_that(value, close_to(0, TOLERANCE))
        value = Thermostat.fahrenheit_to_celsius(212)
        assert_that(value, close_to(100, TOLERANCE))

    def test_celsius_to_fahrenheit(self):
        value = Thermostat.celsius_to_fahrenheit(0)
        assert_that(value, close_to(32, TOLERANCE))
        value = Thermostat.celsius_to_fahrenheit(100)
        assert_that(value, close_to(212, TOLERANCE))

    def test_celsius_to_kelvin(self):
        value = Thermostat.celsius_to_kelvin(0)
        assert_that(value, close_to(273.15, TOLERANCE))
        value = Thermostat.celsius_to_kelvin(100)
        assert_that(value, close_to(373.15, TOLERANCE))

    def test_kelvin_to_celsius(self):
        value = Thermostat.kelvin_to_celsius(273.15)
        assert_that(value, close_to(0, TOLERANCE))
        value = Thermostat.kelvin_to_celsius(373.15)
        assert_that(value, close_to(100, TOLERANCE))


if __name__ == "__main__":
    unittest.main()
