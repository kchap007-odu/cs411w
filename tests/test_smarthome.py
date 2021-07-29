import os
import random
import unittest

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL  # noqa F401
from typing import List
from hamcrest import assert_that, equal_to, is_, same_instance

from smarthome.smarthomes import SmartHome

from helpers.factories import SupportedDevices, device_factory
from helpers.misc import json_from_file, create_logger


class TestSmartHome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Perform these actions once for the entire test case.
        """
        logfile = os.path.join(os.path.dirname(
            __file__), "logs", "test-smarthome.log")
        cls._debug_logger = create_logger(
            filename=logfile,
            file_log_level=INFO,
            standard_out_log_level=ERROR)

        cls.two_thermostats_json = os.path.join(
            os.path.dirname(__file__), 'test-two-thermostats.json')

        cls.test_smart_home_json = os.path.join(
            os.path.dirname(__file__), 'test-smart-home.json')

        cls.test_smart_home_output_json = os.path.join(
            os.path.dirname(__file__), "test-smarthome-output.json")

        cls.devices = ["NestThermostat", "PhilipsHueLamp"]
        cls.types = ["Thermostat", "Light"]
        cls.locations = ["Hallway",
                         "Office", "Upstairs", "Downstairs"]

    def setUp(self):
        """Perform these actions before each test.
        """
        self.default_constructor = SmartHome(logger=self._debug_logger)
        self.config_constructor = SmartHome(json_file=self.two_thermostats_json,
                                            logger=self._debug_logger)

    def test_constructor(self):
        """Tests default and non-default constructors.
        """
        assert_that(len(self.default_constructor), is_(equal_to(0)))
        assert_that(len(self.config_constructor), is_(equal_to(2)))

    def test_add_device(self):
        """
        Tests ability to add devices and verifies related accessors.
        """

        num_devices = random.randrange(1, 50)
        devices: List[SupportedDevices] = []

        for i in range(num_devices):
            device = device_factory(random.choice(self.devices),
                                    config={"location": random.choice(
                                        self.locations)},
                                    logger=self.default_constructor._logger)
            self.default_constructor.append(device)
            devices.append(device)

        # Test __len__ and append
        assert_that(len(self.default_constructor), is_(equal_to(num_devices)))

        # Test search by location
        for location in self.locations:
            assert_that(len(self.default_constructor[{"location": location}]),
                        is_(equal_to(len([device for device in devices
                                          if device.location == location]))))

        # Test search by device id
        for device in devices:
            assert_that(self.default_constructor[device.device_id],
                        is_(same_instance(device)))

        # Test search by device type
        for type_ in self.types:
            assert_that(len(self.default_constructor[{"device_type": type_}]),
                        is_(equal_to(len([device for device in devices
                                          if device.device_type == type_]))))

    def test__from_json__(self):
        """
        Tests ability to write configuration and restore from file.
        """
        json_data = json_from_file(self.test_smart_home_json)

        self.default_constructor.__from_json__(json_data)
        assert_that(len(self.default_constructor), is_(equal_to(3)))

        with open(self.test_smart_home_output_json, "w") as f:
            f.write(str(self.default_constructor))

        smart_home_from_file = SmartHome(
            json_file=self.test_smart_home_output_json,
            logger=self._debug_logger)
        assert_that(str(smart_home_from_file),
                    is_(equal_to(str(self.default_constructor))))


if __name__ == "__main__":
    unittest.main()
