import time
import threading


class Ticker:
    def __init__(self, interval_sec: float, func, *args, **kwargs):
        self.interval = interval_sec
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._stop = threading.Event()

    def start(self):
        next_time = time.time()
        while not self._stop.is_set():
            self.func(self, *self.args, **self.kwargs)
            next_time += self.interval
            sleep_time = next_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                next_time = time.time()

    def stop(self):
        self._stop.set()
