import json
import unittest

from hamcrest import assert_that, equal_to, close_to, is_, is_not, \
    instance_of, same_instance  # noqa: F401
from webservers import HoneywellHome


class TestHoneywellServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_default_constructor = HoneywellHome()
        cls.server_nondefault_constructor = HoneywellHome()
        pass

    def setUp(self):
        pass
