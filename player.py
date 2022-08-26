from threading import Event
import time
from typing import List

from board import Board
from board.DigIn import DigIn

def main():
    event = Event()
    event.set()

    board = Board.instance()
    board.configure_mode()
    digins = board.get_digins()
    show_digins(digins)

    for digin in digins:
        digin.add_activate_event_callback(lambda context: event.set())

    while True:
        event.wait()
        event.clear()

        show_digins(digins)

def show_digins(digins: List[DigIn]):
    for digin in digins:
        print(f"{digin.name}: {'active' if digin.state() else 'inactive'}")


if __name__ == "__main__":
    main()