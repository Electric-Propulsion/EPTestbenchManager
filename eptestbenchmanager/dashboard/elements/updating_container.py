from threading import Lock
from dash import dcc, Input, Output, callback, html

from . import DashboardElement

class UpdatingContainer(DashboardElement):

    def __init__(self, uid: str, title: str, interval: int = 50):
        super().__init__(uid, title)
        self._children = []
        self._lock = Lock()
        self._interval = interval

    @property
    def div(self) -> list:
        return html.Div([
            dcc.Interval(id=f"{self.uid}-interval", interval=self._interval, n_intervals=0),
            html.Div(id=f"{self.uid}-children")
        ])
    
    def add_child(self, child: DashboardElement) -> None:
        with self._lock:
            self._children.append(child)
            child.register_callbacks()
    
    def remove_child(self, child: DashboardElement) -> None:
        with self._lock:
            self._children.remove(child)
            # will not removing callbacks cause a problem?    

    def register_callbacks(self) -> None:
        @callback(
            Output(f"{self.uid}-children", "children"),
            Input(f"{self.uid}-interval", "n_intervals")

        )
        def update_children(n_intervals):
            return [child.div for child in self._children]
    