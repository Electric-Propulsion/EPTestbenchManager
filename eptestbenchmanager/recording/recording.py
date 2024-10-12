from time import monotonic
from typing import Union
from . import Record


class Recording:
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
        self._start_time = None
        self._recording = False
        self._max_display_samples = max_display_samples

    @property
    def active(self):
        if self.max_samples is not None and not self._rolling:
            if len(self._samples) >= self.max_samples:
                return False
        elif self.max_time is not None:
            if monotonic() - self._start_time >= self.max_time:
                return False
        return True

    @property
    def record(self):
        return Record(self._samples, self._max_display_samples)

    def start_recording(self):
        self._start_time = monotonic()
        self._recording = True

    def stop_recording(self):
        self._recording = False

    def add_sample(self, sample):
        self._samples.append(sample)
        if self._rolling and len(self._samples) > self.max_samples:
            self._samples.pop(0)
