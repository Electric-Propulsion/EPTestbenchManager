import time
from typing import Union
from . import Record


class Recording:
    """
    This class represents a recording of time-series data.
    """

    def __init__(
        self,
        max_samples=None,
        max_time_s=None,
        rolling=False,
        max_display_samples=250,  # picked at random lol
    ):
        self.max_samples = max_samples
        self.max_time = max_time_s
        self._rolling = rolling
        self._start_time = None
        self._samples = []
        self._times = []
        self._start_time = None
        self._recording = False
        self._max_display_samples = max_display_samples
        self._using_relative_time = True

    @property
    def active(self):
        if self.max_samples is not None and not self._rolling:
            if len(self._samples) >= self.max_samples:
                return False
        elif self.max_time is not None:
            if time.monotonic() - self._start_time >= self.max_time:
                return False
        return True

    @property
    def record(self):
        return Record(
            self._samples,
            self._times,
            self._using_relative_time,
            self._max_display_samples,
        )

    def start_recording(self):
        self._start_time = (
            time.monotonic()
        )  # this is the only time we use monotonic here, otherwise we care about the actual time
        self._recording = True

    def stop_recording(self):
        self._recording = False

    def add_sample(self, sample, sample_time=None):
        self._samples.append(sample)
        self._times.append(sample_time if sample_time is not None else time.time())
        if self._rolling and len(self._samples) > self.max_samples:
            self._samples.pop(0)
            self._times.pop(0)
