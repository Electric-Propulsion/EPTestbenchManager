from dash import html, dcc
from . import ExperimentElement

class ExperimentStatus(ExperimentElement):

    def div(self):

        progress_bar_marks = {index: name for index, name in ((i, self._experiment.segments[i].uid) for i in len(self._experiment.segments))}

        return html.Div([
            dcc.Slider(marks=progress_bar_marks)
        ])
    
    def register_callbacks(self) -> None:
        return super().register_callbacks()