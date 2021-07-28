import unittest

from hamcrest import assert_that, equal_to, is_, string_contains_in_order

from devices.devices import SmartDevice


class TestDevices(unittest.TestCase):
    def test_constructor(self):
        # Test default constructor.
        d = SmartDevice()
        assert_that(d.name, is_(equal_to("unnamed")))
        assert_that(d.name_long, string_contains_in_order(
            "unnamed", "none", "none"))

        device_id = "1234"
        name = "Device1"
        location = "Hallway"
        # Test non-default constructor
        d = SmartDevice(
            device_id=device_id, name=name, location=location)
        # TODO: Pass and test non-default logger.
        assert_that(d.device_id, is_(equal_to(device_id)))
        assert_that(d.name, is_(equal_to(name)))
        assert_that(d.location, is_(equal_to(location)))
        assert_that(d.name_long, string_contains_in_order(
            name, location))

    def test_set_status(self):
        d = SmartDevice()

        for status in d._statuses:
            d.set_status(status)
            assert_that(d.status, is_(equal_to(status)))

        # TODO: Add test to verify that invalid statuses are rejected.

    def test_set_name(self):
        d = SmartDevice()
        d.set_name("New name")
        assert_that(d.name, is_(equal_to("New name")))

    def test_set_from_json(self):
        d = SmartDevice()

        properties = {"name": "test",
                      "location": "software",
                      "device_id": "abcd",
                      "device_type": "fake",
                      "status": "timer"}
        d.__from_json__(properties)
        for k in properties.keys():
            assert_that(eval(f"d.{k}"), is_(equal_to(properties[k])))

        api_properties = d.__as_json__(properties.keys())
        assert_that(api_properties, is_(equal_to(properties)))

        api_keys = list(d.__api__().keys())
        assert_that(api_keys, is_(equal_to(d._api_return_parameters)))

    def test_set_location(self):
        d = SmartDevice()
        d.set_location("New Location")
        assert_that(d.location, is_(equal_to("New Location")))


if __name__ == "__main__":
    unittest.main()
