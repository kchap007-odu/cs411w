import unittest

import Devices


class TestDevices(unittest.TestCase):
    def test_constructor(self):
        d = Devices.SmartDevice()
        self.assertEqual(d.name, "unnamed")
        self.assertEqual(d.name_long, "unnamed none (none)")
        d = Devices.SmartDevice(device_id="1234")
        self.assertEqual(d.device_id, "1234")

    def test_set_status(self):
        d = Devices.SmartDevice()
        d.set_status("on")
        self.assertEqual(d.status, "on")
        d.set_status("off")
        self.assertEqual(d.status, "off")
        d.set_status("timer")
        self.assertEqual(d.status, "timer")


if __name__ == "__main__":
    unittest.main()
