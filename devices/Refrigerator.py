from random import randrange


class Refrigerator:
    def current_fridge_temperature(self):
        return randrange(30, 35)

    def target_fridge_temperature(self):
        return randrange(35, 40)

    def current_freezer_temperature(self):
        return randrange(5, 10)

    def target_freezer_temperature(self):
        return randrange(0, 4)

    def energy_use(self):
        return randrange(100, 400)


if __name__ == '__main__':
    current_fridge_temperature = randrange(30, 35)
    target_fridge_temperature = randrange(35, 40)
    current_freezer_temperature = randrange(5, 10)
    target_freezer_temperature = randrange(0, 4)
    energy_use = randrange(100, 400)

    print(f"Current Fridge Temperature: {current_fridge_temperature}°F")
    print(f"Target Fridge Temperature: {target_fridge_temperature}°F")
    print(f"Current Freezer Temperature: {current_freezer_temperature}°F")
    print(f"Target Freezer Temperature: {target_freezer_temperature}°F")
    print(f"Energy Use: {energy_use} watts")

    time = ["Fridge_last_on_time", "Fridge_last_off_time", "Freezer_last_on_time", "Freezer_last_off_time"]

    for currentonoff in time:
        hours = randrange(1, 25)
        minutes = randrange(1, 61)
        seconds = randrange(1, 61)
        print(currentonoff + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds))
