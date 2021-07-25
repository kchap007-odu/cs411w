import os
import unittest

from hamcrest import assert_that, equal_to, is_, instance_of

from smarthome.SmartHome import SmartHome
from devices.Thermostat import NestThermostat


class TestSmartHome(unittest.TestCase):
    def test_constructor(self):
        sh = SmartHome()
        assert_that(sh.num_devices, is_(equal_to(0)))

        config_file = os.path.join(
            os.path.dirname(__file__), 'two-thermostats.ini')
        sh = SmartHome(config_name=config_file)
        assert_that(sh.num_devices, is_(equal_to(2)))

    def test_add_device(self):
        t = NestThermostat()

        device_id = t.device_id
        sh = SmartHome()

        sh.add_new_device(t)
        device = sh.get_device_by_device_id(device_id)

        assert_that(device, is_(instance_of(NestThermostat)))

        assert_that(sh.num_devices, is_(equal_to(1)))
        assert_that(t, is_(equal_to(device)))

        # TODO: Add more tests.

    def test_get_devices_by_type(self):
        config_file = os.path.join(
            os.path.dirname(__file__), 'two-thermostats.ini')
        sh = SmartHome(config_name=config_file)
        devices = sh.get_devices_by_type("Thermostat")
        assert_that(len(devices), is_(equal_to(2)))

    def test_write_config(self):
        sh = SmartHome()
        t1 = NestThermostat(name="Nest", location="Hallway")
        t2 = NestThermostat(name="Nest", location="Living Room")
        sh.add_new_device(t1)
        sh.add_new_device(t2)

        assert_that(sh.num_devices, is_(equal_to(2)))


if __name__ == "__main__":
    unittest.main()
