from typing import Union
from operator import gt, lt, ge, le

class ThresholdLastNValues:
    def __init__(self, n: int, initial_value: Union[int, float], operator : Union[gt,lt,ge,le], threshold: Union[int, float]):
        self._values = [initial_value] * n
        self._oldest_index = 0
        self._operator = operator
        self._threshold = threshold
        self._n = n

    def update_evaluate(self, value: Union[int, float]):
        self._values[self._oldest_index] = value
        self._oldest_index = (self._oldest_index + 1) % self._n

        return all(self._operator(value, self._threshold) for value in self._values)