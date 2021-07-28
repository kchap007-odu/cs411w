import os
import unittest

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL  # noqa F401
from hamcrest import assert_that, equal_to, is_, string_contains_in_order, not_

from devices.devices import SmartDevice
from helpers.misc import create_logger


class TestDevices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join(os.path.dirname(__file__),
                               "logs", "test-devices.log")
        cls._device_id = "1234"
        cls._name = "Device1"
        cls._location = "Hallway"
        cls._invalid_statuses = ["inactive", "broken", "error"]
        cls._logger = create_logger(
            filename=logfile, file_log_level=DEBUG,
            standard_out_log_level=CRITICAL)

    def setUp(self):
        self.default_constructor = SmartDevice(logger=self._logger)
        self.non_default_constructor = SmartDevice(
            location=self._location, name=self._name,
            device_id=self._device_id, logger=self._logger)

    def test_constructor(self):
        # Test default constructor.
        assert_that(self.default_constructor.name, is_(equal_to("unnamed")))
        assert_that(self.default_constructor.name_long,
                    string_contains_in_order("unnamed", "none", "none"))

        # Test non-default constructor
        assert_that(self.non_default_constructor.device_id,
                    is_(equal_to(self._device_id)))
        assert_that(self.non_default_constructor.name,
                    is_(equal_to(self._name)))
        assert_that(self.non_default_constructor.location,
                    is_(equal_to(self._location)))
        assert_that(self.non_default_constructor.name_long,
                    string_contains_in_order(self._name, self._location))

    def test_set_status(self):
        for status in self.default_constructor._statuses:
            self.default_constructor.set_status(status)
            assert_that(self.default_constructor.status, is_(equal_to(status)))

        for invalid_status in self._invalid_statuses:
            self.default_constructor.set_status(invalid_status)
            assert_that(self.default_constructor.status,
                        is_(not_(equal_to(invalid_status))))

    def test_set_name(self):
        self.default_constructor.set_name("New name")
        assert_that(self.default_constructor.name, is_(equal_to("New name")))

    def test_set_from_json(self):
        properties = {"name": "test",
                      "location": "software",
                      "device_id": "abcd",
                      "device_type": "fake",
                      "status": "timer"}
        self.default_constructor.__from_json__(properties)
        for k in properties.keys():
            assert_that(eval(f"self.default_constructor.{k}"), is_(
                equal_to(properties[k])))

        api_properties = self.default_constructor.__as_json__(
            properties.keys())
        assert_that(api_properties, is_(equal_to(properties)))

        api_keys = list(self.default_constructor.__api__().keys())
        assert_that(api_keys, is_(
            equal_to(self.default_constructor._api_return_parameters)))

    def test_set_location(self):
        self.default_constructor.set_location("New Location")
        assert_that(self.default_constructor.location,
                    is_(equal_to("New Location")))


if __name__ == "__main__":
    unittest.main()
