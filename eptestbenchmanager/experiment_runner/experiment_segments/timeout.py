from threading import Timer

class Timeout:
    def __init__(self, timeout_s):
        self._timeout_s = timeout_s
        self._timer = None

    def _timeout_handler(self):
        raise TimeoutError(f"Operation timed out after {self._timeout_s} seconds.")

    def __enter__(self):
        self._timer = Timer(self._timeout_s, self._timeout_handler)
        self._timer.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._timer.cancel()
        return exc_type is TimeoutError

    @staticmethod
    def from_minutes(timeout_minutes):
        return timeout_minutes * 60
