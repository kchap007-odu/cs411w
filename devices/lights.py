import logging
from typing import List

from devices.devices import SmartDevice


class PhilipsHueLamp(SmartDevice):

    _device_type = "Light"
    _api_return_parameters = [
        "brightness",
        "rgb_color"
    ]

    def __init__(self, location: str = "none", name: str = "none",
                 logger: logging.Logger = None):
        super().__init__(location=location, name=name, logger=logger)
        self._api_return_parameters = super()._api_return_parameters + \
            self._api_return_parameters

        self.set_rgb_color([255, 255, 255])
        self.set_brightness(1.0)

    @property
    def brightness(self) -> float:
        return self._brightness

    def set_brightness(self, brightness: float = 0.5):
        if 0.0 <= brightness <= 1.0:
            self._brightness = brightness

    @property
    def rgb_color(self) -> List[int]:
        return self._rgb_color

    def set_rgb_color(self, color: List[int] = [255, 255, 255]):
        self._rgb_color = color


class State:

    _alert: str = "none"
    _bri: int = 0
    _ct: int = 0
    _colormode: str = "hs"
    _effect: str = "none"
    _hue: int = 0
    _on: bool = False
    _reachable: bool = False
    _sat: int = 0
    _xy: List[float] = [0.0]

    def __init__(self):
        pass

    @property
    def alert(self) -> str:
        """Getter for device alerts.

        Returns:
            str: The alert message from the device.
        """
        return self._alert

    def set_alert(self, value: str = "none"):
        """Setter

        Args:
            value (str, optional): [description]. Defaults to "none".

        Returns:
            [type]: [description]
        """

    @property
    def on(self) -> bool:
        """Getter for device on state.

        Returns:
            bool: whether the device is on.
        """
        return self._on

    def set_on(self, value: bool = True):
        """Setter for on state.

        Args:
            value (bool, optional): The target device on state.
            Defaults to True.
        """
        if isinstance(value, bool):
            self._on = value


if __name__ == "__main__":
    s = State()
