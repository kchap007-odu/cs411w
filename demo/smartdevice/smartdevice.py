import sys
import os
from flask import Flask

# FIXME: There's no way this is the right way to handle this.
try:
    from devices.thermostats import (NestThermostat,
                                     celsius_to_kelvin,
                                     fahrenheit_to_celsius)
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(__file__) + "/../..")
    from devices.thermostats import (NestThermostat,
                                     celsius_to_kelvin,
                                     fahrenheit_to_celsius)

app = Flask(__name__)

sd = NestThermostat(location="Hallway")
sd.set_label("Nest")
sd.set_hvac_mode("cool")
sd.set_temperature_scale("F")
sd._ambient_temperature = celsius_to_kelvin(
    fahrenheit_to_celsius(65))
sd.set_target_temperature_high(70)
sd.set_target_temperature_low(60)


@app.route("/device", methods=['GET', 'POST'])
def device_json():
    return sd._as_dict()


if __name__ == "__main__":
    app.run()
