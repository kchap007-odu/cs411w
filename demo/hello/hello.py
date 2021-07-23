from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return "<p>Hello, World!</p>"
    elif request.method == 'POST':
        return "<h1>POSTED!</h1>"


@app.route("/device", methods=['GET', 'POST'])
def json_api_test():
    print(__name__)
    return {
        "device": "thermostat",
        "status": "active",
        "temperature": "20",
        "units": "celsius"
    }
