import unittest
from devices.Refrigerator import Refrigerator


class TestRefrigerator(unittest.TestCase):


    def setUp(self):
        self.rf = Refrigerator()

    def test_current_fridge_temperature(self):
        self.assertTrue(self.rf.current_fridge_temperature() >= 30 and self.rf.current_fridge_temperature() <= 35)

    def test_energy_use(self):
        self.assertTrue(self.rf.energy_use() >= 100 and self.rf.energy_use() <= 400)


if __name__ == "__main__":
    unittest.main()