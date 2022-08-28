
import subprocess
from threading import RLock
from typing import Optional

class Vlc(object):
    def __init__(self):
        self._process = None
        self._lock = RLock()
        self._path = None

    def is_running(self) -> bool:
        with self._lock:
            return (self._process is not None) and (self._process.returncode is None)

    def play(self, path: str) -> bool:
        if self.is_running():
            print("Not playing, vlc already running.")
            return False

        with self._lock:
            print(f"Play {path}")
            self._process = subprocess.Popen([ "cvlc", "--fullscreen", "--no-osd", "--play-and-exit", path ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop(self, path: str) -> bool:
        with self._lock:
            if self.is_running() and (self._path == path):
                print(f"Stopping {path}")
                self._process.kill()

    def current_video(self) -> Optional[str]:
        if self.is_running():
            return self._path
        else:
            return None
