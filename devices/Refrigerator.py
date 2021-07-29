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

    results = []
    for x in range(num):

        data = {}

        current_fridge_temperature = randrange(30, 35)
        target_fridge_temperature = randrange(35, 40)
        current_freezer_temperature = randrange(5, 10)
        target_freezer_temperature = randrange(0, 4)
        energy_use = randrange(100, 400)
        fridge_last_on_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
        fridge_last_off_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
        freezer_last_on_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
        freezer_last_off_time = str(randrange(1, 25)) + ":" + str(randrange(1, 61)) + ":" + str(randrange(1, 61))
