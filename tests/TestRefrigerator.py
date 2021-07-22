import unittest
from random import randrange


class TestRefrigerator(unittest.TestCase):
    def setUp(self):
        energy_use = randrange(100, 400)
        self.energy_use = energy_use
        temp_range = randrange(35, 40)
        self.temp_range = temp_range
        model_number = randrange(1000, 9999)
        self.model_number = model_number
        pass

    def test1(self):
        self.assertTrue(True, self.energy_use in range(100, 400))
        self.assertFalse(False, self.energy_use not in range(100, 400))

    def test2(self):
        self.assertTrue(True, self.temp_range in range(35, 40))
        self.assertFalse(False, self.temp_range not in range(35, 40))

    def test3(self):
        self.assertTrue(True, self.model_number in range(1000, 9999))
        self.assertFalse(False, self.model_number not in range(1000, 9999))


if __name__ == "__main__":
    unittest.main()
