import random


class SmartPlugs:
    Status = ["on", "off"]

    def simulate_consumption(self):
        while self.Status == "on":
            connected_device = ["fan", "Tv", "sound_system", "pressing_iron", "lamp"]
            for device in connected_device:
                if device.index("fan"):
                    power_rate = 75
                    duration = random.randint(18, 24)
                    energy_consumption = power_rate * duration
                elif device.index("Tv"):
                    power_rate = 150
                    duration = random.randint(22, 24)
                    energy_consumption = power_rate * duration
                elif device.index("sound_system"):
                    power_rate = 120
                    duration = random.randint(22, 24)
                    energy_consumption = power_rate * duration
                elif device.index("pressing_iron"):
                    power_rate = 110
                    duration = random.randint(8, 10)
                    energy_consumption = power_rate * duration
                elif device.index("lamp"):
                    power_rate = 60
                    duration = random.randint(16, 18)
                    energy_consumption = power_rate * duration
            return energy_consumption
        else:
            return
