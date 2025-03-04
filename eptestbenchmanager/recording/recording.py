import logging
import time
import csv
import os
import atexit
from typing import TYPE_CHECKING
from eptestbenchmanager.dashboard.elements import RecordingGraph

if TYPE_CHECKING:
    from eptestbenchmanager.connections import VirtualInstrument

logger = logging.getLogger(__name__)


class Recording:
    """
    Represents a recording of time-series data.

    Attributes:
        testbench_manager: Global TestbenchManager object.
        virtual_instrument: The virtual instrument associated with this recording.
        experiment_manager: The global experiment manager instance.
        max_samples: The maximum number of samples to record, ever.
        _stored_samples: The number of samples hold for rolling recordings.
        max_time: The maximum time to record.
        _rolling: Whether the recording is rolling.
        t0: The start time for displaying.
        _start_time: The start time of the recording.
        _samples: The list of recorded samples.
        _times: The list of recorded times, in timestamp format
        _display_times: The list of times, in human-readable format.
        _sample_count: The current count of recorded samples.
        _sample_averaging_level: The current level of sample averaging.
        _sample_average: The current average of samples.
        _time_average: The current average of times.
        _sample_average_count: The current count of sample averages.
        _recording: Whether the recording is active.
        _using_relative_time: Whether to use relative time in formatting times for display.
        record_id: The ID of the record.
        file_id: The user-settable ID of the file.
        instrument_uid: The UID of the instrument.
        uid: The UID of the recording.
        name: The name of the recording.
        log_dir: The directory for logs.
        _file_id: The full internal ID of the file.
        graph: The recording graph instance.
    """

    def __init__(
        self,
        testbench_manager,
        record_id: str,
        record_name: str,
        virtual_instrument: "VirtualInstrument",
        max_samples=None,
        stored_samples=250,
        max_time_s=None,
        rolling=False,
        t0=None,
        file_id: str = None,
    ):
        """
        Initializes a new instance of the Recording class.

        Args:
            testbench_manager: Global TestbenchManager object.
            record_id: The ID of the record.
            record_name: The name of the record.
            virtual_instrument: The virtual instrument instance.
            max_samples: The maximum number of samples to record.
            stored_samples: The number of samples to store.
            max_time_s: The maximum time to record.
            rolling: Whether the recording is rolling.
            t0: The start time for displaying.
            file_id: The ID of the file.
            _file: The actual file object.
            _csv_writer: The CSV writer object.
        """
        self.testbench_manager = testbench_manager
        self.virtual_instrument = virtual_instrument
        self.experiment_manager = testbench_manager.runner
        self.max_samples = max_samples
        self._stored_samples = stored_samples
        self.max_time = max_time_s
        self._rolling = rolling
        self.t0 = t0
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
        self.log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
        )
        os.makedirs(self.log_dir, exist_ok=True)
        self._file_id = f"{self.log_dir}/{self.file_id}_{self.instrument_uid}_{time.strftime('%Y%m%d_%H%M%S')}.csv"  # pylint: disable=line-too-long

        self.graph = self.testbench_manager.dashboard.create_element(
            RecordingGraph, (self.uid, self)
        )

        self._file = None  # will be set in start_recording
        self._csv_writer = None  # will be set in start_recording

    @property
    def active(self):
        """
        Checks if the recording is active.

        Returns:
            bool: True if the recording is active, False otherwise.
        """
        if self.max_samples is not None and not self._rolling:
            if self._sample_count >= self.max_samples:
                return False
        elif self.max_time is not None:
            if time.monotonic() - self._start_time >= self.max_time:
                return False
        return self._recording

    @property
    def samples(self):
        """
        Gets the recorded samples.

        Returns:
            list: The list of recorded samples.
        """
        return self._samples

    @property
    def times(self):
        """
        Gets the recorded times.

        Returns:
            list: The list of recorded times.
        """
        return self._times

    @property
    def display_times(self):
        """
        Gets the display times.

        Returns:
            list: The list of display times.
        """
        return self._display_times

    def start_recording(self):
        """
        Starts the recording.
        """
        if self._start_time is None:
            self._start_time = time.monotonic()
        self._recording = True
        if not self._rolling:
            os.makedirs(os.path.dirname(self._file_id), exist_ok=True)
            self._file = open(self._file_id, mode="a", newline="", encoding="utf-8")
            self._csv_writer = csv.writer(self._file, lineterminator="\n")
            if self._file.tell() == 0:
                self._csv_writer.writerow(["Time", "Value", "Segment UID"])
            atexit.register(self.close_record_file)

    def stop_recording(self):
        """
        Stops the recording.
        """
        self._recording = False
        if not self._rolling:
            self.close_record_file()
            atexit.unregister(self.close_record_file)

    def add_sample(self, sample, sample_time=None):
        """
        Adds a sample to the recording.

        Args:
            sample: The sample to add.
            sample_time: The time of the sample.
        """
        timestamp = sample_time if sample_time is not None else time.time()
        current_experiment = self.experiment_manager.get_experiment_current_segment_uid(
            self.experiment_manager.get_current_experiment_uid()
        )
        self._sample_count += 1

        if not self._recording:
            logger.error("Add sample being called when recording is not active")
        if not self._rolling:
            try:
                self._csv_writer.writerow([timestamp, sample, current_experiment])
                self._file.flush()
            except ValueError:
                logger.error("Error writing to file (File closed?)")

        if self._sample_count <= self._stored_samples:
            self._append_sample(sample, timestamp)
        else:
            if self._rolling:
                self._samples.pop(0)
                self._times.pop(0)
                self._append_sample(sample, timestamp)
            else:
                self._sample_average = (
                    self._sample_average * self._sample_average_count + sample
                ) / (self._sample_average_count + 1)
                self._time_average = (
                    self._time_average * self._sample_average_count + timestamp
                ) / (self._sample_average_count + 1)
                self._sample_average_count += 1

                self._samples[-1] = self._sample_average
                self._times[-1] = self._time_average

                if self._sample_average_count == self._sample_averaging_level:
                    self._sample_average_count = 0
                    self._append_sample(self._sample_average, self._time_average)
                if len(self._samples) > 2 * self._stored_samples:
                    for i in range(0, len(self._samples) - 1, 2):
                        self._samples[i] = (self._samples[i] + self._samples[i + 1]) / 2
                        self._times[i] = (self._times[i] + self._times[i + 1]) / 2
                    self._samples = self._samples[::2]
                    self._times = self._times[::2]
                    self._sample_average_count = 0
                    self._sample_averaging_level *= 2

                    self._sample_average = sample
                    self._time_average = timestamp

    def close_record_file(self):
        """
        Closes the record file.
        """
        self._file.flush()
        self._file.close()

    def _append_sample(self, sample, timestamp):
        """
        Appends a sample to the recording.

        Args:
            sample: The sample to append.
            timestamp: The time of the sample.
        """
        self._samples.append(sample)
        self._times.append(timestamp)
        self.graph.append_point(timestamp, sample)
