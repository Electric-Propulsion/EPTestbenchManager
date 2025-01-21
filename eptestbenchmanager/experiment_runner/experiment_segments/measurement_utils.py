from typing import Union
from operator import gt, lt, ge, le


class ThresholdLastNValues:
    """Class to evaluate if the last N values meet a threshold condition.

    Attributes:
        _values (list): List of the last N values.
        _oldest_index (int): Index of the oldest value in the list.
        _operator (Union[gt, lt, ge, le]): Comparison operator.
        _threshold (Union[int, float]): Threshold value.
        _n (int): Number of values to track.
    """

    def __init__(
        self,
        n: int,
        initial_value: Union[int, float],
        operator: Union[gt, lt, ge, le],
        threshold: Union[int, float],
    ):
        """Initializes ThresholdLastNValues with given parameters.

        Args:
            n (int): Number of values to track.
            initial_value (Union[int, float]): Initial value to populate the list.
            operator (Union[gt, lt, ge, le]): Comparison operator.
            threshold (Union[int, float]): Threshold value.
        """
        self._values = [initial_value] * n
        self._oldest_index = 0
        self._operator = operator
        self._threshold = threshold
        self._n = n

    def update_evaluate(self, value: Union[int, float]) -> bool:
        """Updates the list with a new value and evaluates the threshold condition.

        Args:
            value (Union[int, float]): New value to add to the list.

        Returns:
            bool: True if all values meet the threshold condition, False otherwise.
        """
        self._values[self._oldest_index] = value
        self._oldest_index = (self._oldest_index + 1) % self._n

        return all(
            self._operator(float(value), float(self._threshold))
            for value in self._values
        )
