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
        experiment_manager,
        record_id: str,
        instrument_uid: str,
        max_samples=None,
        stored_samples=250, #picked at random
        max_time_s=None,
        rolling=False,
        t0=None, # optional t_0 parameter for displaying based off of a set start time
    ):
        self.experiment_manager = experiment_manager
        self.max_samples = max_samples
        self._stored_samples = stored_samples
        self.max_time = max_time_s
        self._rolling = rolling
        self._t0 = t0
        self._start_time = None
        self._samples = []
        self._times = []
        self._sample_count = 0
        self._sample_averaging_level = 1
        self._sample_average = 0
        self._time_average = 0
        self._sample_average_count = 0
        self._start_time = None
        self._recording = False
        self._using_relative_time = self._rolling
        self.record_id = record_id
        self.instrument_uid = instrument_uid
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs") # what a terrific line of code.
        os.makedirs(self.log_dir, exist_ok=True)
        self._file_id = f"{self.log_dir}/{self.record_id}_{self.instrument_uid}_{time.strftime('%Y%m%d_%H%M%S')}.csv"



    @property
    def active(self):
        if self.max_samples is not None and not self._rolling:
            if self._sample_count >= self.max_samples:
                return False
        elif self.max_time is not None:
            if time.monotonic() - self._start_time >= self.max_time:
                return False
        return self._recording

    @property
    def record(self):
        return Record(
            self._samples,
            self._times,
            self._using_relative_time,
            self._t0,
        )

    def start_recording(self):
        if self._start_time is None:
            self._start_time = (
            time.monotonic()
            )  # this is the only time we use monotonic here, otherwise we care about the actual time
        self._recording = True
        if not self._rolling:
            self._file = open(self._file_id, mode="a", newline="")
            self._csv_writer = csv.writer(self._file, lineterminator='\n' )
            if self._file.tell() == 0:
                self._csv_writer.writerow(["Time", "Value", "Segment UID"])
            atexit.register(self.close_record_file)

    def stop_recording(self):
        self._recording = False
        if not self._rolling:
            self.close_record_file()
            atexit.unregister(self.close_record_file) # I guess there could be a brief window where the file is closed but it's not unregistered

    def add_sample(self, sample, sample_time=None):
        timestamp = sample_time if sample_time is not None else time.time()
        current_experiment = self.experiment_manager.get_experiment_current_segment_uid(self.experiment_manager.get_current_experiment_id())
        self._sample_count += 1

        if not self._recording:
            print("add sample being called when recording is not active")
        if not self._rolling:
            try: 
                self._csv_writer.writerow([timestamp, sample, current_experiment])
                self._file.flush()
            except ValueError:
                print("File closed - should fix this")

        if self._sample_count <= self._stored_samples:
            self._samples.append(sample)
            self._times.append(timestamp)
        else:
            if self._rolling:
                self._samples.pop(0)
                self._times.pop(0)
                self._samples.append(sample)
                self._times.append(timestamp)
            else: 
                self._sample_average = (self._sample_average * self._sample_average_count + sample) / (
                                self._sample_average_count + 1)                
                self._time_average = (self._time_average * self._sample_average_count + timestamp) / (
                                self._sample_average_count + 1)
                self._sample_average_count += 1

                self._samples[-1] = self._sample_average
                self._times[-1] = self._time_average

                if self._sample_average_count == self._sample_averaging_level:
                    self._sample_average_count = 0
                    self._samples.append(self._sample_average)
                    self._times.append(self._time_average)
                if len(self._samples) > 2*self._stored_samples:
                    for i in range(0, len(self._samples)-1, 2):
                        self._samples[i] = (self._samples[i] + self._samples[i + 1]) / 2
                        self._times[i] = (self._times[i] + self._times[i + 1]) / 2
                    self._samples = self._samples[::2]
                    self._times = self._times[::2]
                    self._sample_average_count = 0
                    self._sample_averaging_level *= 2

                    self._sample_average = sample
                    self._time_average = timestamp
        #print(f"record ID: {self.record_id}, sample count: {self._sample_count}, number of samples: {len(self._samples)}, number of times: {len(self._times)}, value: {sample}, average_count: {self._sample_average_count}, average_level: {self._sample_averaging_level}")
    def close_record_file(self):
        self._file.flush()
        self._file.close()
