from dash import dcc, html, Input, Output, callback
import dash_daq as daq
from . import SingleValueDashboardElement


class Gauge(SingleValueDashboardElement):

    @property
    def div(self) -> html.Div:
        return html.Div(
            [
                daq.Gauge(
                    id=f"{self.uid}-gauge",
                    label=self.title,
                ),
                dcc.Interval(
                    id=f"{self.uid}-update-interval",
                    interval=10,
                    n_intervals=0,
                ),
            ]
        )

    def register_callbacks(self) -> None:

        @callback(
            Output(f"{self.uid}-gauge", "value"),
            Input(f"{self.uid}-update-interval", "n_intervals"),
        )
        def update_gauge(value):
            return self._value_callback()
