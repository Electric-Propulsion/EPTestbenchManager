from dash import html, dcc, callback, Input, Output, State
from . import ExperimentElement

class ExperimentStatus(ExperimentElement):

    @property
    def div(self):

        progress_bar_marks = {0: "Waiting"}
        i = 1
        print(self._experiment.segments)
        for segment in self._experiment.segments:
            progress_bar_marks[i] = segment.uid
            i += 1 

        progress_bar_marks[i] = "Finished"
        
        print(f"marks: {progress_bar_marks}")

        return html.Div([
            dcc.Slider(
                0, 
                len(progress_bar_marks)-1,
                marks=progress_bar_marks, 
                disabled=True, 
                id=f"{self.uid}-progress-slider",
                value=0),
            html.Div(
                children=[
                    html.Button(id = f"{self.uid}-button-begin",
                                children="Begin Experiment"),
                    html.Button(id = f"{self.uid}-button-stop",
                                children="Stop Experiment"),
                ],
                style = {"display": "inline-block"}
            ),
            dcc.Interval(
                id=f"{self.uid}-update-interval",
                interval=10,
                n_intervals=0,
            ),
        ])
    
    def register_callbacks(self) -> None:
        print(f"registering callbacks for experiment status!")
        @callback(
            Output(f"{self.uid}-progress-slider", "value"),
            Input(f"{self.uid}-update-interval", "n_intervals"),
        )
        def update_progress_slider(value):
            return self._experiment.current_segment_id
        
        @callback(
            Input(f"{self.uid}-button-begin", 'n_clicks'),
            #prevent_initial_call=True
        )
        def begin_experiment(n_clicks):
            print("button pressed")
            self._experiment.run()
            return