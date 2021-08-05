import os
import random
import unittest
import json

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL  # noqa: F401
# from typing import List
from hamcrest import assert_that, equal_to, is_, same_instance  # noqa: F401

from smarthome import Location

from helpers.factories import device_factory
from helpers.misc import json_from_file, create_logger, path_relative_to_root


class TestLocation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Perform these actions once for the entire test case.
        """
        logfile = path_relative_to_root("logs/test-location.log")
        if os.path.exists(logfile):
            os.remove(logfile)
        cls._debug_logger = create_logger(
            filename=logfile,
            file_log_level=INFO,
            standard_out_log_level=ERROR)

        cls.two_thermostats_json = path_relative_to_root(
            "configs/test-two-thermostats.json")

        cls.test_smart_home_json = path_relative_to_root(
            "configs/test-location.json")

        cls.test_smart_home_output_json = path_relative_to_root(
            "configs/test-smarthome-output.json")

        cls.devices = ["NestThermostat", "PhilipsHueLamp"]
        cls.types = ["Thermostat", "Light"]
        cls.locations = ["Hallway",
                         "Office", "Upstairs", "Downstairs"]

    def setUp(self):
        """Perform these actions before each test.
        """
        self.default_constructor = Location(logger=self._debug_logger)

    def test_constructor(self):
        """Tests default and non-default constructors.
        """
        assert_that(len(self.default_constructor), is_(equal_to(0)))

    def test_add_device(self):
        """
        Tests ability to add devices and verifies related accessors.
        """

        num_devices = random.randrange(1, 50)

        for i in range(num_devices):
            device = device_factory(random.choice(self.devices),
                                    config={"location": random.choice(
                                        self.locations)},
                                    logger=self.default_constructor._logger)
            self.default_constructor.append(device)

        # Test __len__ and append
        assert_that(len(self.default_constructor), is_(equal_to(num_devices)))

    def test__from_json__(self):
        """
        Tests ability to write configuration and restore from file.
        """
        json_data = json_from_file(self.test_smart_home_json)

        self.default_constructor.__from_json__(json_data)
        assert_that(len(self.default_constructor), is_(equal_to(4)))

        config = json.loads(str(self.default_constructor))

        location_from_file = Location(logger=self._debug_logger)
        location_from_file.__from_json__(config)
        assert_that(len(location_from_file), is_(
            equal_to(len(self.default_constructor))))
        # assert_that(str(location_from_file),
        #             is_(equal_to(str(self.default_constructor))))

        assert_that(len(location_from_file["Thermostat"]), is_(equal_to(2)))
        assert_that(len(location_from_file["Light"]), is_(equal_to(1)))
        assert_that(len(location_from_file["Plug"]), is_(equal_to(1)))


if __name__ == "__main__":
    unittest.main()
