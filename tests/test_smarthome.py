import os
import unittest

from hamcrest import assert_that, equal_to, is_, instance_of

from smarthome.SmartHome import SmartHome
from devices.Thermostat import NestThermostat

from helpers.misc import json_from_file


class TestSmartHome(unittest.TestCase):
    def test_constructor(self):
        sh = SmartHome()
        assert_that(len(sh), is_(equal_to(0)))

        config_file = os.path.join(
            os.path.dirname(__file__), 'test-two-thermostats.json')
        sh = SmartHome(json_file=config_file)
        assert_that(len(sh), is_(equal_to(2)))

    def test_add_device(self):
        t = NestThermostat()

        device_id = t.device_id
        sh = SmartHome()

        sh.append(t)
        device = sh[device_id]

        assert_that(device, is_(instance_of(NestThermostat)))

        assert_that(len(sh), is_(equal_to(1)))
        assert_that(t, is_(equal_to(device)))

        # TODO: Add more tests.

    def test_get_devices_by_type(self):
        config_file = os.path.join(
            os.path.dirname(__file__), 'test-smart-home.json')
        sh = SmartHome(json_file=config_file)
        devices = sh.get_devices_by_type("Thermostat")
        assert_that(len(devices), is_(equal_to(2)))

    def test_construct_devices_from_json(self):
        config_file = os.path.join(
            os.path.dirname(__file__), 'test-smart-home.json')
        json_data = json_from_file(config_file)

        sh = SmartHome()
        sh.__from_json__(json_data)
        assert_that(len(sh), is_(equal_to(3)))

    def test_write_config(self):
        sh = SmartHome()
        t1 = NestThermostat(name="Nest", location="Hallway")
        t2 = NestThermostat(name="Nest", location="Living Room")
        sh.append(t1)
        sh.append(t2)
        # print(str(sh))

        assert_that(len(sh), is_(equal_to(2)))


if __name__ == "__main__":
    unittest.main()
