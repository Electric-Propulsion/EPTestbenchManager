from enum import Enum


class AlertSeverity(Enum):
    """
    Enum for the severity of an alert.
    """

    INFO = 1
    CAUTION = 2
    WARNING = 3
