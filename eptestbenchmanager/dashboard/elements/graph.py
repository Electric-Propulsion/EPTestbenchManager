import time
from datetime import timedelta
from dash import dcc, html, Input, Output, callback
import dash_daq as daq
from . import SingleValueDashboardElement
import plotly.graph_objs as go
from dash import dcc, callback, Output, Input


class Graph(SingleValueDashboardElement):
    def __init__(
        self,
        uid: str,
        title: str,
        value_callback: callable,
        update_interval: int = 500,
        num_timestamps: int = 10,
    ):
        super().__init__(uid, title, value_callback)
        self._update_interval = update_interval
        self._num_timestamps = num_timestamps

    @property
    def div(self) -> html.Div:
        return html.Div(
            [
                dcc.Graph(
                    id=f"{self.uid}-graph",
                ),
                dcc.Interval(
                    id=f"{self.uid}-update-interval",
                    interval=self._update_interval,
                    n_intervals=0,
                ),
            ]
        )

    def register_callbacks(self) -> None:

        @callback(
            Output(f"{self.uid}-graph", "figure"),
            Input(f"{self.uid}-update-interval", "n_intervals"),
        )
        def update_graph(n_intervals):
            x_values, y_values = self._value_callback()

            if len(x_values) < self._num_timestamps:
                x_labels_indices = range(len(x_values))
            else:
                step = len(x_values) / self._num_timestamps
                x_labels_indices = [int(i * step) for i in range(self._num_timestamps)]
                x_labels_indices.append(len(x_values) - 1)

            x_labels = [x_values[i] for i in x_labels_indices]

            figure = go.Figure(
                data=[
                    go.Scatter(
                        x=x_values, y=y_values, mode="lines", line_shape="spline"
                    )
                ]
            )
            figure.update_layout(
                xaxis=dict(
                    tickvals=[x_values[i] for i in x_labels_indices],
                    ticktext=x_labels,
                )
            )
            figure.update_layout(template='plotly_dark')

            return figure
