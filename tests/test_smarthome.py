import os
import random
import unittest

from typing import List
from hamcrest import assert_that, equal_to, is_, same_instance

from smarthome.smarthomes import SmartHome
from devices.thermostats import NestThermostat

from helpers.factories import SupportedDevices, device_factory
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
        """
        Tests the ability to add devices and checks related accessors.
        """
        sh = SmartHome()
        possible_devices = ["NestThermostat", "PhilipsHueLamp"]
        possible_device_types = ["Thermostat", "Light"]
        possible_locations = ["Hallway", "Office", "Upstairs", "Downstairs"]

        num_devices = random.randrange(1, 50)
        devices: List[SupportedDevices] = []
        device_types: List[str] = []
        device_ids: List[str] = []
        locations: List[str] = []

        for i in range(num_devices):

            device_type = random.choice(possible_devices)
            location = random.choice(possible_locations)
            device = device_factory(device_type, config={"location": location})

            devices.append(device)
            device_types.append(device_type)
            locations.append(device.location)
            device_ids.append(device.device_id)
            sh.append(device)

        # Test __len__ and append
        assert_that(len(sh), is_(equal_to(num_devices)))

        # Test search by location
        for location in possible_locations:
            assert_that(len(sh[{"location": location}]), is_(
                equal_to(locations.count(location))))

        # Test search by device id
        for idx, id_ in enumerate(device_ids):
            assert_that(sh[id_], is_(same_instance(devices[idx])))

        # Test search by device type
        for device, type_ in zip(possible_devices, possible_device_types):
            assert_that(len(sh[{"device_type": type_}]), is_(
                equal_to(device_types.count(device))))

    def test_get_devices_by_type(self):
        config_file = os.path.join(
            os.path.dirname(__file__), 'test-smart-home.json')
        sh = SmartHome(json_file=config_file)
        # devices = sh.get_devices_by_type("Thermostat")
        properties = {"device_type": "Thermostat"}
        devices = sh[properties]
        assert_that(len(devices), is_(equal_to(2)))

        properties = {"device_type": "Thermostat", "location": "Upstairs"}
        devices = sh[properties]
        assert_that(len(devices), is_(equal_to(1)))

    def test__from_json__(self):
        config_file = os.path.join(
            os.path.dirname(__file__), 'test-smart-home.json')
        json_data = json_from_file(config_file)

        sh = SmartHome()
        sh.__from_json__(json_data)
        assert_that(len(sh), is_(equal_to(3)))

    def test_write_config(self):
        # TODO: Make this test actually do something.
        sh = SmartHome()
        t1 = NestThermostat(name="Nest", location="Hallway")
        t2 = NestThermostat(name="Nest", location="Living Room")
        sh.append(t1)
        sh.append(t2)

        assert_that(len(sh), is_(equal_to(2)))


if __name__ == "__main__":
    unittest.main()
