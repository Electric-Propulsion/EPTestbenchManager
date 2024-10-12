from . import DashboardElement


class SingleValueDashboardElement(DashboardElement):
    def __init__(
        self,
        uid: str,
        title: str,
        value_callback: callable,
    ):
        super().__init__(uid, title)
        self._value_callback = value_callback
