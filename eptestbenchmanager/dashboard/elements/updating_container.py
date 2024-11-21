from threading import Lock, Semaphore, BoundedSemaphore
from dash import dcc, Input, Output, callback, html, no_update

from . import DashboardElement

class UpdatingContainer(DashboardElement):

    def __init__(self, uid: str, title: str, interval: int = 250):
        super().__init__(uid, title)
        self._children = []
        self._lock = Lock()
        self._updates = BoundedSemaphore(1)
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
            try:
                self._updates.release()
            except ValueError:
                pass #expected behavior :(
    
    def remove_child(self, child: DashboardElement) -> None:
        with self._lock:
            self._children.remove(child)
            # will not removing callbacks cause a problem?
            try:
                self._updates.release()
            except ValueError:
                pass #expected behavior :(

    def register_callbacks(self) -> None:
        @callback(
            Output(f"{self.uid}-children", "children"),
            Input(f"{self.uid}-interval", "n_intervals")

        )
        def update_children(n_intervals):
            if self._updates.acquire(blocking=False):
                with self._lock:
                    return [child.div for child in self._children]
            else:
                return no_update
    