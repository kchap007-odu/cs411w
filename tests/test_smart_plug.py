import unittest
import json
import os

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL  # noqa F401

from hamcrest import assert_that, close_to, contains_string, equal_to, is_,\
    is_not, string_contains_in_order

from devices import SmartPlug
from helpers.misc import create_logger


class TestSmartPlug(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sp = SmartPlug()

    def test__from_json__(self):
        config = {
            "is_on": True,
            "name": "plug"
        }
        self.sp.__from_json__(config)
        assert_that(self.sp.is_on, is_(equal_to(True)))
        assert_that(self.sp.name, is_(equal_to("plug")))


if __name__ == "__main__":
    unittest.main()


