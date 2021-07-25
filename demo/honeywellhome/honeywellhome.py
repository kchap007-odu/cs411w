import sys

from flask import Flask

from smarthome.SmartHome import SmartHome

app = Flask(__name__)
sh = SmartHome(config_name="home-1.ini")

# --------------------------- AUTHORIZATION -------------------------- #


@app.route("/accesstoken", methods=["POST"])
def get_access_token():
    pass


@app.route("/authorize", methods=["GET"])
def get_authorization():
    return "authorization code"


@app.route("/token", methods=["POST"])
def get_token():
    pass

# -------------------------- THERMOSTAT ------------------------------ #


@app.route("/devices", methods=['GET', 'POST'])
def get_devices():
    lst = [f"{d.device_type}: {d.device_id}" for d in sh.devices]
    return "<br>".join(lst)


@app.route("/devices/<device_type>", methods=["GET"])
def get_devices_by_type(device_type):
    if device_type == "thermostats":
        devices = sh.get_devices_by_type("Thermostat")
    elif device_type == "lights":
        devices = sh.get_devices_by_type("Light")

    lst = [f"{d.device_type}: {d.device_id}" for d in devices]
    return "<br>".join(lst)


@app.route("/devices/<device_type>/<device_id>", methods=["GET"])
def do_subpath(device_type, device_id):
    device = sh.get_device_by_device_id(device_id)
    print(device)
    return device.as_dict()


@app.route("/locations", methods=["GET"])
def get_locations():
    pass


if __name__ == "__main__":
    print(sys.argv)
    app.run()
