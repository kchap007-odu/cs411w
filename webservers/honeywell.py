import sys
import flask

from flask import jsonify, abort, request

from typing import List

from smarthome import Location
from helpers.misc import json_from_file, path_relative_to_root


class HoneywellHome(flask.Flask):
    def __init__(self, config_filename=None):
        super().__init__(__name__)
        self._locations: List[Location] = []
        self.route("/")(self.by_location)
        self.route("/locations")(self.by_location)
        self.route("/devices")(self.by_device)
        self.route("/devices/<device_type>")(self.by_device_type)
        self.route("/devices/<device_type>/<device_id>",
                   methods=["GET", "POST"])(self.by_device_id)

        if config_filename is not None:
            self.__from_json__(json_from_file(config_filename))

    def __from_json__(self, config: dict):
        for location in config:
            new_location = Location()
            new_location.__from_json__(location)
            self._locations.append(new_location)

    def __to_json__(self):
        result = []
        for location in self._locations:
            result.append(location.__to_json__())
        return result

    def by_location(self):
        return jsonify(self.__to_json__())

    def _by_device(self):
        devices = {}
        for location in self._locations:
            for device in location._devices:
                devices[device.device_id] = device.__as_json__(
                    device._api_return_parameters)
        return devices

    def _by_device_type(self, device_type):
        devices = self._by_device()
        return {k: v for k, v in devices.items()
                if v["device_type"] == device_type}

    def by_device(self):
        return jsonify(self._by_device())

    def by_device_type(self, device_type):
        return jsonify(self._by_device_type(device_type))

    def by_device_id(self, device_type, device_id):

        if request.method == "POST":
            for location in self._locations:
                for device in location._devices:
                    if device["device_id"] == device_id:
                        device.__from_json__(request.json)

        devices = self._by_device_type(device_type)
        for k, v in devices.items():
            if v["device_id"] == device_id:
                return v

        abort(404)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        config = sys.argv[1]
    else:
        config = "configs/default-home.json"
    # Force file to be relative to project root.
    full_path = path_relative_to_root(config)
    app = HoneywellHome(full_path)
    app.run()
