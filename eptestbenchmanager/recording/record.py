from typing import Union, Tuple
import time
from datetime import timedelta


class Record:
    def __init__(
        self,
        values: list[Union[str, int, float, bool]],
        times: list[
            Union[str, int, float]
        ],  # These are always assumed to be *entered* as UNIX timestamps
        relative: bool = False,
        max_display_values: int = 250,
    ):
        self._values = values
        self._times = times
        self._relative = (
            relative  # Relative to whenever the all or display property is called
        )
        self._max_display_values = max_display_values
        self._length = len(values)

    @property
    def all(self) -> list[Union[str, int, float, bool]]:
        if self._relative:
            time_now = time.time()
            return [
                (self._times[i] - time_now, self._values[i])
                for i in range(self._length)
            ]
        return self._times.copy(), self._values.copy()

    @property
    def display(
        self,
    ) -> Tuple[list[Union[str, int, float, bool]], list[Union[str, int, float]]]:
        if self._length <= self._max_display_values:
            values = self._values.copy()
            times = self._times.copy()
        else:
            step = self._length / self._max_display_values
            values = []
            times = []
            for i in range(self._max_display_values):
                start = int(i * step)
                end = int((i + 1) * step)
                value_chunk = self._values[start:end]
                # time_chunk = self._times[start:end]
                if value_chunk:
                    values.append(sum(value_chunk) / len(value_chunk))
                    # if time_chunk:
                    times.append(self._times[int(start + (end - start) / 2)])
        # Format all timestamps based on the relative flag
        if self._relative:
            time_now = time.time()
            times = [time_now - t for t in times]
        else:
            times = [t for t in times]

        if self._relative:
            times = [self._format_relative_time(t) for t in times]
        else:
            times = [self._format_absolute_time(t) for t in times]
        return times, values

    def _format_relative_time(self, delta: float) -> str:
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

    def _format_absolute_time(self, timestamp: float) -> str:
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
            return f"T+{days} days, {hours:02}:{minutes:02}:{seconds:02}.{millis:03}"
        else:
            return f"T+{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"

    def __len__(self) -> int:
        return self._length

    @property
    def length(self) -> int:
        return self.__len__()
