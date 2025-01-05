import time
from datetime import timedelta
import csv
import os
import atexit
from typing import Union
from eptestbenchmanager.dashboard.elements import RecordingGraph


class Recording:
    """
    This class represents a recording of time-series data.
    """

    def __init__(
        self,
        testbench_manager, # experiment_manager
        record_id: str,
        record_name: str,
        virtual_instrument: "VirtualInstrument",
        max_samples=None,
        stored_samples=250, #picked at random
        max_time_s=None,
        rolling=False,
        t0=None, # optional t_0 parameter for displaying based off of a set start time
        file_id: str = None
    ):
        self.testbench_manager = testbench_manager
        self.virtual_instrument = virtual_instrument
        self.experiment_manager = testbench_manager.runner
        self.max_samples = max_samples
        self._stored_samples = stored_samples
        self.max_time = max_time_s
        self._rolling = rolling
        self._t0 = t0
        self._start_time = None
        self._samples = []
        self._times = []
        self._display_times = []
        self._sample_count = 0
        self._sample_averaging_level = 1
        self._sample_average = 0
        self._time_average = 0
        self._sample_average_count = 0
        self._start_time = None
        self._recording = False
        self._using_relative_time = self._rolling
        self.record_id = record_id
        self.file_id = file_id
        self.instrument_uid = virtual_instrument.uid
        self.uid = f"{self.instrument_uid}_{record_id}"
        self.name = f"{self.virtual_instrument.name} {record_name}"
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs") # what a terrific line of code.
        os.makedirs(self.log_dir, exist_ok=True)
        self._file_id = f"{self.log_dir}/{self.file_id}_{self.instrument_uid}_{time.strftime('%Y%m%d_%H%M%S')}.csv"

        self.graph = self.testbench_manager.dashboard.create_element(RecordingGraph, (self.uid, self))


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
    def samples(self):
        return self._samples
    
    @property
    def times(self):
        return self._times
    
    @property
    def display_times(self):
        return self._display_times

    def start_recording(self):
        if self._start_time is None:
            self._start_time = (
            time.monotonic()
            )  # this is the only time we use monotonic here, otherwise we care about the actual time
        self._recording = True
        if not self._rolling:
            os.makedirs(os.path.dirname(self._file_id), exist_ok=True)
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
            self._append_sample(sample, timestamp)
        else:
            if self._rolling:
                self._samples.pop(0)
                self._times.pop(0)
                self._append_sample(sample, timestamp)
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
                    self._append_sample(self._sample_average, self._time_average)
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
                    
    def close_record_file(self):
        self._file.flush()
        self._file.close()

    def _format_relative_time(self, timestamp: float) -> str:
        delta = time.time() - timestamp
        delta_td = timedelta(seconds=delta)
        days = delta_td.days
        hours, minutes, seconds = (
            delta_td.seconds // 3600,
            (delta_td.seconds // 60) % 60,
            delta_td.seconds % 60,
        )
        millis = delta_td.microseconds // 1000
        if days > 0:
            return f"T-{days} days, {hours:02}:{minutes:02}:{seconds:02}.{millis:03}"
        else:
            return f"T-{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"

    def _format_absolute_time(self, timestamp: float, t0: float) -> str:
        abs_time = timestamp - t0
        days, hours, minutes, seconds, millis = (
            abs_time // 86400,
            abs_time // 3600,
            (abs_time // 60) % 60,
            abs_time % 60,
            (abs_time * 1000) % 1000,
        )
        if days > 0:
            return f"T+{days:.0f} days, {hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}.{millis:03.0f}"
        else:
            return f"T+{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}.{millis:03.0f}"


    def _append_sample(self, sample, timestamp):
        self._samples.append(sample)
        self._times.append(timestamp)
        if self._using_relative_time:
            label = self._format_relative_time(timestamp) 
        else:
            label = self._format_absolute_time(timestamp, self._t0 if self._t0 is not None else self._times[0])
        self._display_times.append(label)
        self.graph.append_point(timestamp, sample, label)
