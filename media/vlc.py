
import os
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
            running = (self._process is not None) and (self._process.returncode is None)

            print(f"Process running: {running}")
            print(f"process active: {self._process is not None}")
            print(f"returncode: {'not running' if self._process is None else self._process.returncode}")
            print("----")

            return running

    def play(self, path: str) -> bool:
        return self.__play(path, False)

    def play_loop(self, path: str) -> bool:
        return self.__play(path, True)

    def __play(self, path: str, loop: bool = False) -> bool:
        with self._lock:
            if self.is_running():
                print("Not playing, vlc already running.")
                return False

            if not os.path.exists(path):
                print(f"'{path}' does not exists!")
                return False

            if not os.path.isfile(path):
                print(f"'{path}' is not a file!")
                return False


            print(f"Play {path}")
            cmd = [ "cvlc", "--fullscreen", "--no-osd", "--play-and-exit" ]
            cmd.append("-V")
            cmd.append("drm_vout")

            if loop:
                cmd.append("--loop")

            cmd.append(path)
            self._process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._path = path

    def stop(self, path: str) -> bool:
        with self._lock:
            print(f"{self.is_running()} '{self._path}' == '{path}'")

            if self.is_running() and (self._path == path):
                print(f"Stopping {path}")
                self._process.terminate()

                try:
                    self._process.wait(2.0)
                except subprocess.TimeoutExpired:
                    self._process.kill()

                self._process = None

    def current_video(self) -> Optional[str]:
        if self.is_running():
            return self._path
        else:
            return None

    def wait(self):
        if self._process is not None:
            self._process.wait()
