import unittest
from random import randrange


class TestRefrigerator(unittest.TestCase):
    def setUp(self):
        energy_use = randrange(100, 400)
        self.energy_use = energy_use
        target_fridge = randrange(35, 40)
        self.temp_range = target_fridge
        current_fridge = randrange(30, 35)
        self.temp_range = current_fridge
        current_freezer = randrange(5, 10)
        self.temp_range = current_freezer
        target_freezer = randrange(0, 4)
        self.temp_range = target_freezer
        model_number = randrange(1000, 9999)
        self.model_number = model_number
        pass

    def test1(self):
        self.assertTrue(True, self.energy_use in range(100, 400))
        self.assertFalse(False, self.energy_use not in range(100, 400))

    def test2(self):
        self.assertTrue(True, self.target_fridge in range(35, 40))
        self.assertFalse(False, self.target_fridge not in range(35, 40))

    def test3(self):
        self.assertTrue(True, self.current_fridge in range(30, 35))
        self.assertFalse(False, self.current_fridge not in range(30, 35))

    def test4(self):
        self.assertTrue(True, self.current_freezer in range(5, 10))
        self.assertFalse(False, self.current_freezer not in range(5, 10))

    def test5(self):
        self.assertTrue(True, self.target_freezer in range(0, 4))
        self.assertFalse(False, self.target_freezer not in range(0, 4))

    def test6(self):
        self.assertTrue(True, self.model_number in range(1000, 9999))
        self.assertFalse(False, self.model_number not in range(1000, 9999))


if __name__ == "__main__":
    unittest.main()
