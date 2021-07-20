from random import randrange


class Refrigerator:
    def __init__(self, current_fridge_temperature, target_fridge_temperature, current_freezer_temperature,
                 target_freezer_temperature, energy_use):
        self.current_fridge_temperature = current_fridge_temperature
        self.target_fridge_temperature = target_fridge_temperature
        self.current_freezer_temperature = current_freezer_temperature
        self.target_freezer_temperature = target_freezer_temperature
        self.energy_use = energy_use

    time = ["Fridge_last_on_time", "Fridge_last_off_time", "Freezer_last_on_time", "Freezer_last_off_time"]

    for currentonoff in time:
        hours = randrange(1, 25)
        minutes = randrange(1, 61)
        seconds = randrange(1, 61)
        print(currentonoff + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds))
