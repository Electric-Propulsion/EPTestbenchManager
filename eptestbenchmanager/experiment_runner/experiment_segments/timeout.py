from threading import Timer, Event


class Timeout:
    """A context manager for handling timeouts using threading.Timer.

    Attributes:
        _timeout_s (float): The timeout duration in seconds.
        _timer (Timer): The timer object.
        timeout_expired (Event): Event that signals if the timeout has expired.
    """

    def __init__(self, timeout_s):
        """Initializes the Timeout with a specified duration.

        Args:
            timeout_s (float): The timeout duration in seconds.
        """
        self._timeout_s = timeout_s
        self._timer = None
        self.timeout_expired = Event()

    def _timeout_handler(self):
        """Handles the timeout event by setting the timeout_expired event."""
        self.timeout_expired.set()

    def __enter__(self):
        """Starts the timer when entering the context.

        Returns:
            Timeout: The Timeout instance.
        """
        self._timer = Timer(self._timeout_s, self._timeout_handler)
        self._timer.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cancels the timer when exiting the context.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception instance.
            traceback (traceback): The traceback object.

        Returns:
            bool: True if the exception is TimeoutError, False otherwise.
        """
        self._timer.cancel()
        return exc_type is TimeoutError

    @property
    def expired(self):
        """Checks if the timeout has expired.

        Returns:
            bool: True if the timeout has expired, False otherwise.
        """
        return self.timeout_expired.is_set()

    @staticmethod
    def from_minutes(timeout_minutes):
        """Converts minutes to seconds.

        Args:
            timeout_minutes (float): The timeout duration in minutes.

        Returns:
            float: The timeout duration in seconds.
        """
        return timeout_minutes * 60
