from threading import Timer, Event

class Timeout:
    def __init__(self, timeout_s):
        self._timeout_s = timeout_s
        self._timer = None
        self.timeout_expired = Event()

    def _timeout_handler(self):
        self.timeout_expired.set()

    def __enter__(self):
        self._timer = Timer(self._timeout_s, self._timeout_handler)
        self._timer.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._timer.cancel()
        return exc_type is TimeoutError
    
    @property
    def expired(self):
        return self.timeout_expired.is_set()


    @staticmethod
    def from_minutes(timeout_minutes):
        return timeout_minutes * 60
