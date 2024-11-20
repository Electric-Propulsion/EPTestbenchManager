from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
import time, datetime

from . import ExperimentElement


class ExperimentStatus(ExperimentElement):

    def __init__(
        self,
        uid: str,
        title: str,
        testbench_manager: "TestbenchManager",
        experiment_uid: str,
    ):
        super().__init__(uid, title, testbench_manager, experiment_uid)
        self.operator = None

    @property
    def div(self):

        progress_bar_marks = {-1: "Waiting"}
        i = 0
        for segment in self._experiment_runner.get_experiment_segments(
            self._experiment_uid
        ):
            progress_bar_marks[i] = segment.uid
            i += 1

        progress_bar_marks[i] = "Finished"

        print(f"marks: {progress_bar_marks}")

        return html.Div(
            [
                dcc.Slider(
                    -1,
                    len(progress_bar_marks) - 2,
                    marks=progress_bar_marks,
                    disabled=True,
                    id=f"{self.uid}-progress-slider",
                    value=0,
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id=f"{self.uid}-operator-dropdown",
                            multi=True,
                            placeholder="Select Operator(s)",
                        ),
                        html.Button(
                            id=f"{self.uid}-button-begin", children="Begin Experiment"
                        ),
                        html.Button(
                            id=f"{self.uid}-button-stop", children="Stop Experiment"
                        ),
                    ],
                    style={"display": "inline-block", "text_align": "center"},
                ),
                dcc.Interval(
                    id=f"{self.uid}-update-interval",
                    interval=10,
                    n_intervals=0,
                ),   
            ]
        )

    def register_callbacks(self) -> None:
        print(f"registering callbacks for experiment status!")

        @callback(
            Output(f"{self.uid}-progress-slider", "value"),
            Input(f"{self.uid}-update-interval", "n_intervals"),
        )
        def update_progress_slider(value):
            return self._experiment_runner.get_experiment_current_segment_id(
                self._experiment_uid
            )

        @callback(
            Input(f"{self.uid}-button-begin", "n_clicks"),
            # prevent_initial_call=True
        )
        def begin_experiment(n_clicks):
            print("button pressed")
            if self.operator is not None:
                self._experiment_runner.run_experiment(
                    self._experiment_uid, self.operator
                )
            else:
                print("No operator selected")

        @callback(
            Output(f"{self.uid}-operator-dropdown", "options"),
            Input(f"{self.uid}-operator-dropdown", "value"),
        )
        def update_options(value):
            return [*self._available_operators.keys()] #TODO: quick fix. Make this dynamic.

        @callback(
            Input(f"{self.uid}-operator-dropdown", "value"),
        )
        def update_operator(value):
            print(f"Operator selected: {value}")
            self.operator = value
            return
