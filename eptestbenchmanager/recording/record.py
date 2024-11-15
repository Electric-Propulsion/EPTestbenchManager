from typing import Union, Tuple
import time
from datetime import timedelta, date
import datetime


class Record:
    def __init__(
        self,
        values: list[Union[str, int, float, bool]],
        times: list[
            Union[str, int, float]
        ],  # These are always assumed to be *entered* as UNIX timestamps
        relative: bool = False,
    ):
        self._values = values
        self._times = times
        self._relative = (
            relative  # Relative to whenever the all or display property is called
        )
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
        if self._relative:
            times = [self._format_relative_time(time, 0) for time in self._times]
        else:
            times = [self._format_absolute_time(time, self._times[0]) for time in self._times]
    
        return times, self._values.copy()
    

    def _format_relative_time(self, timestamp: float, t_now: float) -> str:
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

    def __len__(self) -> int:
        return self._length

    @property
    def length(self) -> int:
        return self.__len__()
