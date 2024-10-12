from dash import dcc, html, Input, Output, callback
import dash_daq as daq
from . import SingleValueDashboardElement
import plotly.graph_objs as go


class Graph(SingleValueDashboardElement):

    def __init__(
        self,
        uid: str,
        title: str,
        value_callback: callable,
        update_interval: int = 50,
    ):
        super().__init__(uid, title, value_callback)
        self._update_interval = update_interval

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
            values = self._value_callback()

            # Calculate the x-axis values
            x_values = [
                f"T-{(len(values) - 1 - i) * self._update_interval}"
                for i in range(len(values))
            ]

            # Ensure there are always 10 labels
            num_labels = 10
            step = max(1, len(x_values) // (num_labels - 1))
            x_labels = [""] * len(x_values)

            # Ensure T-0 is always on the right
            if len(x_values) > 0:
                x_values[-1] = "T-0"
                x_labels[-1] = "T-0"

            # Add labels at regular intervals, ensuring they are at least 10% away from T-0
            last_label_index = len(x_values) - 1
            for i in range(len(x_values) - 2, -1, -step):
                if last_label_index - i >= len(x_values) * 0.1:
                    x_labels[i] = x_values[i]
                    last_label_index = i

            figure = go.Figure(
                data=[
                    go.Scatter(x=x_values, y=values, mode="lines", line_shape="spline")
                ]
            )
            figure.update_layout(
                xaxis=dict(
                    tickvals=[i for i, label in enumerate(x_labels) if label],
                    ticktext=[label for label in x_labels if label],
                )
            )
            return figure
