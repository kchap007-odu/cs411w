import unittest

from flask import app  # noqa: F401
from hamcrest import assert_that, is_, not_, instance_of, equal_to, \
    close_to  # noqa: F401

from demo.honeywellhome import honeywellhome


class TestHonewellHome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._get_paths = [
            "/authorize", "/devices", "/devices/thermostats",
            "/devices/thermosats/<deviceid>/fan", ""
        ]
        cls.app = honeywellhome.app.test_client()


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._valid_get_paths = [
            "/", "/authorize", "/locations",
            "/devices", "/devices/thermostats", "/devices/lights",
            "/devices/refrigerators", "/devices/faucets",
            "/devices/plugs", "/devices/waterheaters"]
        cls._invalid_paths = [
            "/nonexistent", "/nonexistent/path", "/path/does/not/exist"
        ]
        cls._post_paths = [
            "/devices", "/token", "/accesstoken"
        ]
        cls.app = honeywellhome.app.test_client()

    def test_response_codes(self):
        for path in self._valid_get_paths:
            response = self.app.get(path)
            assert_that(response.status_code, is_(equal_to(200)))
            # print(response.json)

        for path in self._invalid_paths:
            response = self.app.get(path)
            assert_that(response.status_code, is_(equal_to(404)))

        for path in self._post_paths:
            response = self.app.post(path)
            assert_that(response.status_code, is_(equal_to(200)))

    def test_json_receive(self):

        response = self.app.get("/devices")
        assert_that(response.json, is_(instance_of(dict)))
        assert_that(len(response.json), is_(equal_to(3)))

    def test_post(self):
        self.app.post("/devices", json={"test": "value"})


if __name__ == "__main__":
    unittest.main()
