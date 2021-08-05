import os
import sys
import random
import json

from flask import Flask

# FIXME: There's no way this is the right way to handle this.
try:
    from smarthome.smarthomes import SmartHome
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(__file__) + "/../..")
    from smarthome.smarthomes import SmartHome


app = Flask(__name__)
config_name = os.path.normpath(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "../../configs/home-1.json"))
sh = SmartHome(json_file=config_name)

# --------------------------- AUTHORIZATION -------------------------- #


@ app.route("/accesstoken", methods=["POST"])
def get_access_token():
    return "Here's your access token: 1234"


@ app.route("/authorize", methods=["GET"])
def get_authorization():
    return "authorization code"


@ app.route("/token", methods=["POST"])
def get_token():
    return "here's your token: O"

# ---------------------------- DEVICES ------------------------------- #


@ app.route("/")
def get_config():
    return json.loads(str(sh))


@ app.route("/devices", methods=['GET', 'POST'])
def get_devices():
    # if request.method == "POST":
    # print("Posted")
    return {
        f"device{i}": j.__api__() for (i, j) in enumerate(sh._devices, start=1)
    }


@ app.route("/devices/<device_type>", methods=["GET"])
def get_devices_by_type(device_type):
    path_translations = {
        "thermostats": "Thermostat",
        "lights": "Light",
        "refrigerators": "Refrigerator",
        "faucets": "Faucet",
        "plugs": "Plug",
        "waterheaters": "WaterHeater"
    }
    devices = sh[{"device_type": path_translations[device_type]}]

    return {
        f"device{i}": j.__api__() for (i, j) in enumerate(devices, start=1)
    }


@ app.route("/devices/<device_type>/<device_id>", methods=["GET"])
def do_subpath(device_type, device_id):
    device = sh[device_id]
    device._ambient_temperature = random.randint(293, 300)
    device._humidity = random.random()
    return device.__api__()


@ app.route("/locations", methods=["GET"])
def get_locations():
    return str(sh)


if __name__ == "__main__":
    app.run()
