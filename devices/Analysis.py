import random

from flask import Flask, render_template
from devices import SmartPlug


app = Flask(__name__)

app.route("/")

def home():
    duration = random.randint(12, 24)
    _data = (SmartPlug.power_draw(), duration)

    labels = [row[0] for row in _data]
    values = [row[1] for row in _data]

    return render_template("graph.html", labels = labels, values = values)

