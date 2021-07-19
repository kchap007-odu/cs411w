import random
import datetime


class Refrigerator:
    def __init__(self, current_fridge_temperature, target_fridge_temperature, current_freezer_temperature,
                 target_freezer_temperature, fridge_last_on_time, fridge_last_off_time, freezer_last_on_time,
                 freezer_last_off_time, energy_use):
        self.current_fridge_temperature = current_fridge_temperature
        self.target_fridge_temperature = target_fridge_temperature
        self.current_freezer_temperature = current_freezer_temperature
        self.target_freezer_temperature = target_freezer_temperature
        self.fridge_last_on_time = fridge_last_on_time
        self.fridge_last_off_time = fridge_last_off_time
        self.freezer_last_on_time = freezer_last_on_time
        self.freezer_last_off_time = freezer_last_off_time
        self.energy_use = energy_use
