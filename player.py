from threading import Event
import time
from typing import List

from board import Board
from board.DigIn import DigIn
from media.vlc import Vlc

VIDEO_BTN1 = "/home/pi/Media/video1.mp4"
VIDEO_BTN2 = "/home/pi/Media/video2.mp4"
VIDEO_SWITCH = "/home/pi/Media/video_switch.mp4"

vlc = Vlc()
event = Event()

def main():
    event.set()

    board = Board.instance()
    board.configure_mode()
    digins = board.get_digins()
    show_digins(digins)

    board.get_button1().add_activate_event_callback(play_movie1)
    board.get_button2().add_activate_event_callback(play_movie2)
    board.get_switch().add_activate_event_callback(play_movie_loop)
    board.get_switch().add_deactivate_event_callback(stop_movie_loop)

    # Just some handlers to let the following while loop run once in a while
    board.get_button1().add_activate_event_callback(lambda context: event.set())
    board.get_button2().add_activate_event_callback(lambda context: event.set())
    board.get_switch().add_activate_event_callback(lambda context: event.set())

    while True:
        event.wait()
        event.clear()

        show_digins(digins)

def play_movie1(*args, **kwargs):
    vlc.play(VIDEO_BTN1)

def play_movie2(*args, **kwargs):
    vlc.play(VIDEO_BTN2)

def play_movie_loop(*args, **kwargs):
    vlc.play(VIDEO_SWITCH)

def stop_movie_loop(*args, **kwargs):
    vlc.stop(VIDEO_SWITCH)

def show_digins(digins: List[DigIn]):
    for digin in digins:
        print(f"{digin.name}: {'active' if digin.state() else 'inactive'}")


if __name__ == "__main__":
    main()