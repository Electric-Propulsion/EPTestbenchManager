from ..dashboardelement import DashboardElement
from flask_socketio import Namespace, emit, SocketIO
from flask import render_template

class RecordingGraph(DashboardElement):
    class RecordingGraphNamespace(Namespace):
        def on_connect(self):
            print(f"New client connected to GraphNamespace {self.element.namespace}")
            self.element.update()

        def __init__(self, namespace, element):
            super().__init__(namespace)
            self.element = element


    def __init__(self, uid: str, recording: 'Recording', socketio: SocketIO = None):
        super().__init__(uid, socketio)
        self.recording = recording
        self._rolling = self.recording._rolling
        self._max_points = self.recording._stored_samples if self._rolling else 0
        self.namespace = f"/{uid}"
        self.socketio.on_namespace(self.RecordingGraphNamespace(self.namespace, self))

    def render_html(self):
        data = {
            "uid": self.uid
        }
        return render_template("elements/recording_graph.html", data=data)
    
    def render_js(self):
        data = {
            "namespace": self.namespace,
            "uid": self.uid,
            "rolling": self._rolling,
            "max_points": self._max_points,
            "name": self.recording.name,
            "measurement_name" : self.recording.virtual_instrument.name,
            "measurement_unit" : self.recording.virtual_instrument.unit
        }
        print(data)
        return render_template("elements/recording_graph.js", data=data)
    
    def append_point(self, h_axis_datapoint, v_axis_datapoint):
        self.socketio.emit("append_point", {"h_axis_datapoint": h_axis_datapoint, "v_axis_datapoint": v_axis_datapoint}, namespace=self.namespace)

    def update(self):
        h_axis_data = self.recording.times
        v_axis_data = self.recording.samples
        self.socketio.emit("update", {"h_axis_data": h_axis_data, "v_axis_data": v_axis_data}, namespace=self.namespace)

    