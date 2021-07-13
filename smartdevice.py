from flask import Flask
# from flask import request
# from flask import jsonify

import Devices

app = Flask(__name__)

sd = Devices.Thermostat()


@app.route("/device", methods=['GET', 'POST'])
def device_json():
    return sd.as_dict()
