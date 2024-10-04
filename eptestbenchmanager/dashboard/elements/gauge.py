from dash import dcc, html, Input, Output, callback
import dash_daq as daq
from .dashboard_element import DashboardElement
import random


class Gauge(DashboardElement):

    @property
    def div(self) -> html.Div:
        return html.Div(
            [
                daq.Gauge(
                    id=f"{self.uid}-gauge",
                    label=self.title,
                ),
                dcc.Interval(
                    id=f"{self.uid}-interval",
                    interval=10,
                    n_intervals=0,
                ),
            ]
        )

    def register_callbacks(self) -> None:

        @callback(
            Output(f"{self.uid}-gauge", "value"),
            Input(f"{self.uid}-interval", "n_intervals"),
        )
        def update_gauge(value):
            return random.randint(0, 100)
