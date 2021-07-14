import unittest
import datetime

import Thermostat


class TestThermostats(unittest.TestCase):
    def test_constructor(self):
        t = Thermostat.NestThermostat()
        self.assertEqual(t.name_long, "none Thermostat (none)")

        t = Thermostat.NestThermostat(name="Nest", location="Living Room")
        self.assertEqual(t.name_long, "Nest Thermostat (Living Room)")

    def test_set_temperature_scale(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        self.assertEqual(t.temperature_scale, "F")

        t.set_temperature_scale("C")
        self.assertEqual(t.temperature_scale, "C")

        t.set_temperature_scale("K")
        self.assertEqual(t.temperature_scale, "K")

    def test_set_fan_timer_duration(self):
        t = Thermostat.NestThermostat()

        t.set_fan_timer_duration(value=10)
        self.assertEqual(t.fan_timer_duration, datetime.timedelta(minutes=10))

        t.set_fan_timer_duration(value=60)
        self.assertEqual(t.fan_timer_duration, datetime.timedelta(minutes=60))

    def test_set_eco_temperature_high(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_eco_temperature_high(value=70)
        self.assertEqual(t.eco_temperature_high_f, 70)

        t.set_temperature_scale("C")
        t.set_eco_temperature_high(value=30)
        self.assertEqual(t.eco_temperature_high_c, 30)

        t.set_temperature_scale("K")
        t.set_eco_temperature_high(value=290)
        self.assertEqual(t._eco_temperature_high, 290)

    def test_set_eco_temperature_low(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_eco_temperature_low(value=70)
        self.assertEqual(t.eco_temperature_low_f, 70)

        t.set_temperature_scale("C")
        t.set_eco_temperature_low(value=30)
        self.assertEqual(t.eco_temperature_low_c, 30)

        t.set_temperature_scale("K")
        t.set_eco_temperature_low(value=290)
        self.assertEqual(t._eco_temperature_low, 290)

    def test_set_hvac_mode(self):
        t = Thermostat.NestThermostat()

        # Test default values. These may change.
        self.assertEqual(t.hvac_mode, "off")
        self.assertEqual(t.previous_hvac_mode, "")

        t.set_hvac_mode(value="cool")
        self.assertEqual(t.hvac_mode, "cool")
        self.assertEqual(t.previous_hvac_mode, "off")

        t.set_hvac_mode(value="heat")
        self.assertEqual(t.hvac_mode, "heat")
        self.assertEqual(t.previous_hvac_mode, "cool")

        t.set_hvac_mode(value="eco")
        self.assertEqual(t.hvac_mode, "eco")
        self.assertEqual(t.previous_hvac_mode, "heat")

        t.set_hvac_mode(value="heat-cool")
        self.assertEqual(t.hvac_mode, "heat-cool")
        self.assertEqual(t.previous_hvac_mode, "eco")

        t.set_hvac_mode(value="off")
        self.assertEqual(t.hvac_mode, "off")
        self.assertEqual(t.previous_hvac_mode, "heat-cool")

    def test_set_is_locked(self):
        t = Thermostat.NestThermostat()

        # Test the default value.
        self.assertFalse(t.is_locked)

        t.set_is_locked(value=True)
        self.assertTrue(t.is_locked)

        t.set_is_locked(value=False)
        self.assertFalse(t.is_locked)

    def test_set_locked_temp_max(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_locked_temp_max(value=90)
        self.assertEqual(t.locked_temp_max_f, 90)

        t.set_temperature_scale("C")
        t.set_locked_temp_max(value=30)
        self.assertEqual(t.locked_temp_max_c, 30)

        t.set_temperature_scale("K")
        t.set_locked_temp_max(value=290)
        self.assertEqual(t._locked_temp_max, 290)

    def test_set_locked_temp_min(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_locked_temp_min(value=60)
        self.assertEqual(t.locked_temp_min_f, 60)

        t.set_temperature_scale("C")
        t.set_locked_temp_min(value=10)
        self.assertEqual(t.locked_temp_min_c, 10)

        t.set_temperature_scale("K")
        t.set_locked_temp_min(value=260)
        self.assertEqual(t._locked_temp_min, 260)

    def test_set_target_temperature_high(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_target_temperature_high(value=90)
        self.assertEqual(t.target_temperature_high_f, 90)

        t.set_temperature_scale("C")
        t.set_target_temperature_high(value=30)
        self.assertEqual(t.target_temperature_high_c, 30)

        t.set_temperature_scale("K")
        t.set_target_temperature_high(value=290)
        self.assertEqual(t._target_temperature_high, 290)

    def test_set_target_temperature_low(self):
        t = Thermostat.NestThermostat()

        t.set_temperature_scale("F")
        t.set_target_temperature_low(value=60)
        self.assertEqual(t.target_temperature_low_f, 60)

        t.set_temperature_scale("C")
        t.set_target_temperature_low(value=10)
        self.assertEqual(t.target_temperature_low_c, 10)

        t.set_temperature_scale("K")
        t.set_target_temperature_low(value=260)
        self.assertEqual(t._target_temperature_low, 260)

    def test_set_label(self):
        t = Thermostat.NestThermostat()

        t.set_label("Test")
        self.assertTrue("Test" in t.name_long)

        t.set_label("New")
        self.assertTrue("New" in t.name_long)

    def test_fahrenheit_to_celsius(self):
        value = Thermostat.fahrenheit_to_celsius(32)
        self.assertEqual(value, 0)
        value = Thermostat.fahrenheit_to_celsius(212)
        self.assertEqual(value, 100)

    def test_celsius_to_fahrenheit(self):
        value = Thermostat.celsius_to_fahrenheit(0)
        self.assertEqual(value, 32)
        value = Thermostat.celsius_to_fahrenheit(100)
        self.assertEqual(value, 212)

    def test_celsius_to_kelvin(self):
        value = Thermostat.celsius_to_kelvin(0)
        self.assertEqual(value, 273.15)
        value = Thermostat.celsius_to_kelvin(100)
        self.assertEqual(value, 373.15)

    def test_kelvin_to_celsius(self):
        value = Thermostat.kelvin_to_celsius(273.15)
        self.assertEqual(value, 0)
        value = Thermostat.kelvin_to_celsius(373.15)
        self.assertEqual(value, 100)


if __name__ == "__main__":
    unittest.main()
