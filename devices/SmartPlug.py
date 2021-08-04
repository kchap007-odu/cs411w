import random
import datetime
import logging

from devices.devices import SmartDevice


class SmartPlug(SmartDevice):

    _api_return_parameters = [
        "power_draw",
        "is_on",
        "last_on_time",
        "last_off_time"
    ]

    _power_draw_ranges = [
        lambda: random.randint(108, 112),
        lambda: random.randint(145, 155)
    ]

    _device_type = "Plug"

    def __init__(self, logger: logging.Logger = logging.getLogger("dummy")):
        super().__init__(logger=logger)
        self._pick_power_range()
        self.set_is_on()
        self.set_last_on_time(datetime.datetime.now())
        self.set_last_off_time(datetime.datetime.now())
        self._api_return_parameters = super()._api_return_parameters + \
            self._api_return_parameters

    @ property
    def is_on(self):
        return self._is_on

    def set_is_on(self, value: bool = False):
        self._is_on = value

    @ property
    def last_on_time(self):
        return self._last_on_time.isoformat()

    def set_last_on_time(self, value: datetime.datetime):
        self._last_on_time = datetime.datetime.now()

    @ property
    def last_off_time(self):
        return self._last_off_time.isoformat()

    def set_last_off_time(self, value: datetime.datetime):
        self._last_off_time = datetime.datetime.now()
        - datetime.timedelta(minutes=5)

    @ property
    def power_draw(self):
        return self._power_range()

    def _pick_power_range(self):
        self._power_range = random.choice(self._power_draw_ranges)


if __name__ == "__main__":
    sp = SmartPlug()
    print(sp.last_on_time)
    print(sp.last_off_time)
    print(sp.is_on)
    for i in range(1, 5):
        print(sp.power_draw)

    print(sp.__properties__())
