import unittest

from hamcrest import assert_that, close_to, is_

from helpers.unitconverters import (celsius_to_fahrenheit, celsius_to_kelvin,
                                    kelvin_to_celsius, fahrenheit_to_celsius)


class TestTemperatureConverters(unittest.TestCase):

    _tolerance = 1e-10
    _temps_k = [
        0, 5, 10, 15,
        20, 30, 40, 50,
        100, 150, 200, 250,
        500, 1000, 1500, 2000
    ]
    _temps_c = [
        -273.15, -268.15, -263.15, -258.15,
        -253.15, -243.15, -233.15, -223.15,
        -173.15, -123.15, -73.15, -23.15,
        226.85, 726.85, 1226.85, 1726.85
    ]
    _temps_f = [
        -459.67, -450.67, -441.67, -432.67,
        -423.67, -405.67, -387.67, -369.67,
        -279.67, -189.67, -99.67, -9.67,
        440.33, 1340.33, 2240.33, 3140.33
    ]

    def test_fahrenheit_to_celsius(self):

        for (f, c) in zip(self._temps_f, self._temps_c):
            assert_that(
                fahrenheit_to_celsius(f), is_(close_to(c, self._tolerance))
            )

    def test_celsius_to_fahrenheit(self):
        for (c, f) in zip(self._temps_c, self._temps_f):
            assert_that(
                celsius_to_fahrenheit(c), is_(close_to(f, self._tolerance))
            )

    def test_celsius_to_kelvin(self):
        for (c, k) in zip(self._temps_c, self._temps_k):
            assert_that(
                celsius_to_kelvin(c), is_(close_to(k, self._tolerance))
            )

    def test_kelvin_to_celsius(self):
        for (k, c) in zip(self._temps_k, self._temps_c):
            assert_that(
                kelvin_to_celsius(k), is_(close_to(c, self._tolerance))
            )


if __name__ == "__main__":
    unittest.main()
