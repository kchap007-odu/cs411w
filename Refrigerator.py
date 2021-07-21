from random import randrange


class Refrigerator:
    def __init__(self, current_fridge_temperature, target_fridge_temperature, current_freezer_temperature,
                 target_freezer_temperature, energy_use):
        self.current_fridge_temperature = current_fridge_temperature
        self.target_fridge_temperature = target_fridge_temperature
        self.current_freezer_temperature = current_freezer_temperature
        self.target_freezer_temperature = target_freezer_temperature
        self.energy_use = energy_use


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
