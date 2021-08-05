import os
import json
import logging
import unittest

from hamcrest import assert_that, close_to, is_, equal_to, \
    string_contains_in_order

from helpers.unitconverters import (celsius_to_fahrenheit, celsius_to_kelvin,
                                    kelvin_to_celsius, fahrenheit_to_celsius)

from helpers.misc import create_logger, log_message_formatter, json_from_file, \
    path_relative_to_root, get_device_translations  # noqa: F401


class TestTemperatureConverters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set these up once per test case.
        """
        cls._tolerance = 1e-10
        cls._temps_k = [
            0, 5, 10, 15,
            20, 30, 40, 50,
            100, 150, 200, 250,
            500, 1000, 1500, 2000
        ]
        cls._temps_c = [
            -273.15, -268.15, -263.15, -258.15,
            -253.15, -243.15, -233.15, -223.15,
            -173.15, -123.15, -73.15, -23.15,
            226.85, 726.85, 1226.85, 1726.85
        ]
        cls._temps_f = [
            -459.67, -450.67, -441.67, -432.67,
            -423.67, -405.67, -387.67, -369.67,
            -279.67, -189.67, -99.67, -9.67,
            440.33, 1340.33, 2240.33, 3140.33
        ]

    def test_fahrenheit_to_celsius(self):
        """Test conversion from Fahrenheit to Celsius.
        """

        for (f, c) in zip(self._temps_f, self._temps_c):
            assert_that(
                fahrenheit_to_celsius(f), is_(close_to(c, self._tolerance))
            )

    def test_celsius_to_fahrenheit(self):
        """Test conversion from Celsius to Fahrenheit.
        """
        for (c, f) in zip(self._temps_c, self._temps_f):
            assert_that(
                celsius_to_fahrenheit(c), is_(close_to(f, self._tolerance))
            )

    def test_celsius_to_kelvin(self):
        """Test conversion from Celsius to Kelvin.
        """
        for (c, k) in zip(self._temps_c, self._temps_k):
            assert_that(
                celsius_to_kelvin(c), is_(close_to(k, self._tolerance))
            )

    def test_kelvin_to_celsius(self):
        """Test conversion from Kelvin to Celsius.
        """
        for (k, c) in zip(self._temps_k, self._temps_c):
            assert_that(
                kelvin_to_celsius(k), is_(close_to(c, self._tolerance))
            )


class TestMiscellaneousFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_path_relative_to_root(self):
        """Tests conversion from relative path to absolute path.
        """
        full_path = path_relative_to_root(
            "tests/files/file-exists.py")
        assert_that(os.path.exists(full_path), is_(True))

    def test_create_logger(self):
        """Tests ability to create loggers.
        """
        file_level = logging.ERROR
        stream_level = logging.CRITICAL
        logger = create_logger(
            filename="test-logger.log",
            file_log_level=file_level,
            standard_out_log_level=stream_level)
        file_handlers = [
            h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        stream_handlers = [
            h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert_that(len(file_handlers), is_(equal_to(1)))
        assert_that(file_handlers[0].level, is_(equal_to(file_level)))
        # File handler is subclass of stream handler.
        assert_that(len(stream_handlers), is_(equal_to(2)))
        assert_that(stream_handlers[1].level, is_(equal_to(stream_level)))

        # TODO: Finish writing this test. Possibly check that creating a
        # second logger does not interfere with the first.

        pass

    def test_log_message_formatter(self):
        """Tests logger message formatting.
        """
        get_set = "set"
        device_id = "1234"
        property_ = "my_property"
        value = "abcd"
        message = log_message_formatter(get_set=get_set, device_id=device_id,
                                        property_=property_, value=value)
        assert_that(message, string_contains_in_order(
            get_set, device_id, property_, f"'{value}'", "."))
        value = 123

        message = log_message_formatter(get_set=get_set, device_id=device_id,
                                        property_=property_, value=value)
        assert_that(message, string_contains_in_order(
            get_set, device_id, property_, f"{value}", "."))

    def test_json_from_file(self):
        """Tests conversion of JSON file to Python dictionary.
        """
        abs_path = path_relative_to_root("configs/test-json-from-file.json")
        config = {"test": "value"}
        with open(abs_path, "w") as f:
            f.write(json.dumps(config, indent=4))

        with open(abs_path, "r") as f:
            config_from_file = json_from_file(abs_path)

        os.remove(abs_path)

        assert_that(config_from_file, is_(equal_to(config)))

    def test_get_device_translations(self):
        """Tests translation from url device name to device classes.
        """
        pass


if __name__ == "__main__":
    unittest.main()
