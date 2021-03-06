from random import randrange
import json

from devices.devices import SmartDevice


class Refrigerator(SmartDevice):

    _api_return_parameters = [
        "target_fridge_temperature",
        "current_fridge_temperature",
        "current_freezer_temperature",
        "target_freezer_temperature",
        "energy_use"
    ]
    _device_type = "Refrigerator"

    def __init__(self, logger=None):
        self._logger = logger
        super().__init__()
        self._api_return_parameters = self._api_return_parameters \
            + super()._api_return_parameters

    @ property
    def current_fridge_temperature(self):
        return randrange(30, 35)

    @ property
    def target_fridge_temperature(self):
        return randrange(35, 40)

    @ property
    def current_freezer_temperature(self):
        return randrange(5, 10)

    @ property
    def target_freezer_temperature(self):
        return randrange(0, 4)

    @ property
    def energy_use(self):
        return randrange(100, 400)


if __name__ == '__main__':
    num = 5
    # defining an empty list
    results = []
    for x in range(num):
        # creating an empty dict
        data = {}
        # defining all the attributes needed, using random numbers
        current_fridge_temperature = randrange(30, 35)
        target_fridge_temperature = randrange(35, 40)
        current_freezer_temperature = randrange(5, 10)
        target_freezer_temperature = randrange(0, 4)
        energy_use = randrange(100, 400)
        fridge_last_on_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
        fridge_last_off_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
        freezer_last_on_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
        freezer_last_off_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
        # adding each attribute to data dict, with proper key (name of attribute)
        data["Current Fridge Temperature"] = current_fridge_temperature
        data["Target Fridge Temperature"] = target_fridge_temperature
        data["Current Freezer Temperature"] = current_freezer_temperature
        data["Target Freezer Temperature"] = target_freezer_temperature
        data["Energy Use"] = energy_use
        data["Fridge Last On Time"] = fridge_last_on_time
        data["Fridge Last Off Time"] = fridge_last_off_time
        data["Freezer Last On Time"] = freezer_last_on_time
        data["Freezer Last Off Time"] = freezer_last_off_time
        # adding data dict to results list
        results.append(data)
    # printing results list of dicts in json format, with 4 as indentation
    print(json.dumps(results, indent=4))

    # outputs json file
    f = open('data_chart.json', 'w')
    json.dump(results, f)
    f.close()
