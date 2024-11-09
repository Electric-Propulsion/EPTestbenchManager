import time
import csv
import os
import atexit
from typing import Union
from . import Record


class Recording:
    """
    This class represents a recording of time-series data.
    """

    def __init__(
        self,
        record_id: str,
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
        self.record_id = record_id
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs") # what a terrific line of code.
        os.makedirs(self.log_dir, exist_ok=True)


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
        
        if not self._rolling:
            file_id = f"{self.log_dir}/{self.record_id}_{time.strftime('%Y%m%d_%H%M%S')}.csv"
            self._file = open(file_id, mode="a", newline="")
            self._csv_writer = csv.writer(self._file, lineterminator='\n' )
            if self._file.tell() == 0:
                self._csv_writer.writerow(["Time", "Value"])
            atexit.register(self.close_record_file)

    def stop_recording(self):
        self._recording = False
        if not self.rolling:
            self.close_record_file()
            atexit.unregister(self.close_record_file) # I guess there could be a brief window where the file is closed but it's not unregistered

    def add_sample(self, sample, sample_time=None):
        timestamp = sample_time if sample_time is not None else time.time()
        self._samples.append(sample)
        self._times.append(timestamp)
        if self._rolling and len(self._samples) > self.max_samples:
            self._samples.pop(0)
            self._times.pop(0)

        if not self._rolling:
            self._csv_writer.writerow([timestamp, sample])
            self._file.flush()

    def close_record_file(self):
        self._file.flush()
        self._file.close()
