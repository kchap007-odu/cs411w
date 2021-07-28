import unittest
from devices.Refrigerator import Refrigerator


class TestRefrigerator(unittest.TestCase):

    # setup method
    def setUp(self):
        self.rf = Refrigerator()

    # below 5 methods are for individual variables
    # assertTrue() calls function and check if return value matches condition or not. If matches, asserts true else asserts false
    def test_current_fridge_temperature(self):
        self.assertTrue(self.rf.current_fridge_temperature() >= 30 and self.rf.current_fridge_temperature() <= 35)

    def test_target_fridge_temperature(self):
        self.assertTrue(self.rf.target_fridge_temperature() >= 35 and self.rf.target_fridge_temperature() <= 40)

    def test_current_freezer_temperature(self):
        self.assertTrue(self.rf.current_freezer_temperature() >= 5 and self.rf.current_freezer_temperature() <= 10)

    def test_target_freezer_temperature(self):
        self.assertTrue(self.rf.target_freezer_temperature() >= 0 and self.rf.target_freezer_temperature() <= 4)

    def test_energy_use(self):
        self.assertTrue(self.rf.energy_use() >= 100 and self.rf.energy_use() <= 400)


# main to call unittest
if __name__ == "__main__":
    unittest.main()
