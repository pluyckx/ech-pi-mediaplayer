import threading
import time
from typing import Callable, List, Optional
import RPi.GPIO as GPIO

class DigIn(object):
    def __init__(self, id: int, name: str, active_high=False):
        """
        Initialize a new DigIn object. The application should not use this constructor directly.
        Use the function `instance` in this module to fetch the DigIn.

        @param id   BUTTON1, BUTTON2, SWITCH
        """
        self._id = id
        self._state = None
        self.active_high = active_high
        self.name = name
        self.__timer = None

        GPIO.setup(self._id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._id, GPIO.BOTH)
        GPIO.add_event_callback(self._id, __Callable(lambda: self.__restart()))
        self._activate_event_callbacks = []
        self._deactivate_event_callbacks = []

        self.update()

    def state(self) -> Optional[bool]:
        return self._state

    def __restart(self):
        if self.__timer is not None:
            self.__timer.cancel()

        # print(f"Restart timer for digin {self.name}")
        self.__timer = threading.Timer(0.1, __Callable(lambda: self.update()))
        self.__timer.start()

    def update(self):
        # print(f"Update digin {self.name}")
        old_state = self.state()

        state = GPIO.input(self._id)

        if state:
            self._state = True if self.active_high else False
        else:
            self._state = False if self.active_high else True

        state = self.state()

        if (state != old_state) and (old_state is not None):
            if state:
                DigIn._fire_event(self._activate_event_callbacks, self)
            else:
                DigIn._fire_event(self._deactivate_event_callbacks, self)

    def add_activate_event_callback(self, callback: Callable):
        if not callable(callback):
            raise Exception("Expected a callable callback!")

        self._activate_event_callbacks.append(callback)

    def add_deactivate_event_callback(self, callback: Callable):
        if not callable(callback):
            raise Exception("Expected a callable callback!")

        self._deactivate_event_callbacks.append(callback)

    @staticmethod
    def _fire_event(callbacks: List[Callable], context):
        for callback in callbacks:
            callback(context)

# Append with _DigIn because python will append this when using `__StateChange` in the code above.
class _DigIn__Callable(object):
    def __init__(self, callable: Callable):
        self._callable = callable

    def __call__(self, *args, **kwargs):
        self._callable()
