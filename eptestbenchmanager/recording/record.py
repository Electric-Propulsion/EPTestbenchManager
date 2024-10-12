from typing import Union


class Record:
    def __init__(
        self, values: list[Union[str, int, float, bool]], max_display_values: int = 250
    ):
        self._values = values
        self._max_display_values = max_display_values
        self._length = len(values)

    @property
    def values(self) -> list[Union[str, int, float, bool]]:
        return self._values.copy()

    @property
    def display_values(self) -> list[Union[str, int, float, bool]]:
        if self._length <= self._max_display_values:
            return self._values.copy()
        else:
            step = self._length / self._max_display_values
            compressed_values = []
            for i in range(self._max_display_values):
                start = int(i * step)
                end = int((i + 1) * step)
                chunk = self._values[start:end]
                if chunk:
                    compressed_values.append(sum(chunk) / len(chunk))
            return compressed_values

    def __len__(self) -> int:
        return self._length

    @property
    def length(self) -> int:
        return self.__len__()
