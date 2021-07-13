from typing import List

import Devices


class Light(Devices.SmartDevice):
    _rgb_color = [255, 255, 255]
    _brightness = 1.0

    def __init__(self):
        super().__init__()
        pass

    @property
    def brightness(self) -> float:
        return self._brightness

    def set_brightness(self, brightness: float = 0.5):
        if 0.0 < brightness < 1.0:
            self._brightness = brightness

    def set_rgb_color(self, color: List(int) = [255, 255, 255]):
        pass
