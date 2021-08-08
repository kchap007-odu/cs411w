# import json
import unittest
import logging

from hamcrest import assert_that, equal_to, close_to, is_, is_not, \
    instance_of, same_instance, contains_string  # noqa: F401
from webservers import HoneywellHome


class TestHoneywellServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._get_routes = [
            "/",
            "/locations",
            "/devices",
            "/devices/Thermostat",
            "/devices/Light",
            "/devices/Plug",
            "/devices/Refrigerator",
            "/devices/Thermostat/1234",
            "/devices/Light/2345",
            "/devices/Plug/3456",
            "/devices/Refrigerator/4567"
        ]

        cls._post_routes = [
            "/devices/Thermostat/1234",
            "/devices/Light/2345",
            "/devices/Plug/3456",
            "/devices/Refrigerator/4567"
        ]

        cls.server_default_constructor = HoneywellHome(
            config_filename="configs/default-home.json")
        cls.server_nondefault_constructor = HoneywellHome(
            config_filename="configs/simple.json")

        logging.disable(logging.WARNING)

    def setUp(self):
        pass

    def test_constructors(self):
        assert_that(len(self.server_default_constructor._locations),
                    is_(equal_to(2)))

    def test_responses(self):
        for get_route in self._get_routes:
            with self.server_default_constructor.test_client() as c:
                resp = c.get(get_route)
                assert_that(resp.status_code, is_(equal_to(200)))

        for post_route in self._post_routes:
            with self.server_default_constructor.test_client() as c:
                resp = c.post(get_route, json={"test": "value"})
                assert_that(resp.status_code, is_(equal_to(200)))

    def test_response_data(self):
        pass

    def test_post(self):
        pass
