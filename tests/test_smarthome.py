import os
import unittest

from hamcrest import assert_that, equal_to, is_, instance_of

from smarthome.SmartHome import SmartHome
from devices.Thermostat import NestThermostat
from devices.Light import PhilipsHueLamp


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
        device = sh.get_device_by_device_id(device_id)

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

    def test_get_device_by_id(self):
        config_file = os.path.join(
            os.path.dirname(__file__), 'test-smart-home.json')
        sh = SmartHome(json_file=config_file)

        device = sh["1234"]
        assert_that(device, is_(instance_of(NestThermostat)))
        assert_that(device.device_id, is_(equal_to("1234")))

        device2 = sh["2345"]
        assert_that(device2, is_(instance_of(NestThermostat)))
        assert_that(device2.device_id, is_(equal_to("2345")))

        device3 = sh["3456"]
        assert_that(device3, is_(instance_of(PhilipsHueLamp)))
        assert_that(device3.device_id, is_(equal_to("3456")))

        device_does_not_exist = sh["4567"]
        assert_that(device_does_not_exist, is_(None))

    def test_construct_devices_from_json(self):
        config_file = os.path.join(
            os.path.dirname(__file__), 'test-smart-home.json')
        sh = SmartHome()
        sh._construct_devices_from_json(filename=config_file)
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
