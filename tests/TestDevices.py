import unittest

from devices import Devices


class TestDevices(unittest.TestCase):
    def test_constructor(self):
        # Test default constructor.
        d = Devices.SmartDevice()
        self.assertEqual(d.name, "unnamed")
        self.assertEqual(d.name_long, "unnamed none (none)")

        # Test non-default constructor
        d = Devices.SmartDevice(
            device_id="1234", name="Device1", location="Hallway")
        # TODO: Pass and test non-default logger.
        self.assertEqual(d.device_id, "1234")
        self.assertEqual(d.name, "Device1")
        self.assertEqual(d.location, "Hallway")

    def test_set_status(self):
        d = Devices.SmartDevice()
        d.set_status("on")
        self.assertEqual(d.status, "on")
        d.set_status("off")
        self.assertEqual(d.status, "off")
        d.set_status("timer")
        self.assertEqual(d.status, "timer")

    def test_set_name(self):
        d = Devices.SmartDevice()
        d.set_name("New name")
        self.assertTrue(d.name == "New name")

    def test_set_location(self):
        d = Devices.SmartDevice()
        d.set_location("New Location")
        self.assertTrue(d.location == "New Location")


if __name__ == "__main__":
    unittest.main()
