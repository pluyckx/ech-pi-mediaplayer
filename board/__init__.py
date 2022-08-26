from typing import List
import RPi.GPIO as GPIO
from board.DigIn import DigIn

_board = None


class Board(object):
    DIGIN_BUTTON1 = 0
    DIGIN_BUTTON2 = 1
    DIGIN_SWITCH = 2

    __DIGIN_PINS = [3, 5, 7]

    def __init__(self):
        if _board is not None:
            raise Exception(
                "Not allowed to create a second board! Use `Board::instance()` to get the Board object."
            )

        self.configure_mode()

        self._digins = [
            DigIn(Board.__DIGIN_PINS[Board.DIGIN_BUTTON1], "Button1"),
            DigIn(Board.__DIGIN_PINS[Board.DIGIN_BUTTON2], "Button2"),
            DigIn(Board.__DIGIN_PINS[Board.DIGIN_SWITCH], "Switch"),
        ]

    def configure_mode(self):
        if GPIO.getmode() != GPIO.BOARD:
            GPIO.setmode(GPIO.BOARD)

    def get_digins(self) -> List[DigIn]:
        return self._digins

    def get_digin(self, digin: int) -> DigIn:
        return self._digins[digin]

    def get_button1(self) -> DigIn:
        return self.get_digin(Board.DIGIN_BUTTON1)

    def get_button2(self) -> DigIn:
        return self.get_digin(Board.DIGIN_BUTTON2)

    def get_switch(self) -> DigIn:
        return self.get_digin(Board.DIGIN_SWITCH)

    @staticmethod
    def instance():
        return _board


_board = Board()
