from flask import Flask
# from flask import request
# from flask import jsonify

import Thermostat

app = Flask(__name__)

sd = Thermostat.NestThermostat(location="Hallway")
sd.set_label("Nest")
sd.set_hvac_mode("cool")
sd.set_temperature_scale("F")
sd._ambient_temperature = Thermostat.celsius_to_kelvin(
    Thermostat.fahrenheit_to_celsius(65))
sd.set_target_temperature_high(70)
sd.set_target_temperature_low(60)


@app.route("/device", methods=['GET', 'POST'])
def device_json():
    return sd.as_dict()
