import urllib.request
import json
import datetime


start_time = datetime.datetime.now()
i = 0

while (True):
    if (datetime.datetime.now() - start_time) > datetime.timedelta(seconds=1):
        response = urllib.request.urlopen(
            "http://127.0.0.1:5000/devices/thermostats/1234")
        start_time = datetime.datetime.now()
        i += 1
        print(json.dumps(json.loads(response.read()), indent=4))
    if i == 5:
        break
