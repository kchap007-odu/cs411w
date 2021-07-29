from random import randrange
import json

class Refrigerator:
    def current_fridge_temperature(self):
        return randrange

    def target_fridge_temperature(self):
        return randrange

    def current_freezer_temperature(self):
        return randrange

    def target_freezer_temperature(self):
        return randrange

    def energy_use(self):
        return randrange


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
