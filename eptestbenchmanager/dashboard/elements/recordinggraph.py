from ..dashboardelement import DashboardElement
from flask_socketio import Namespace, emit, SocketIO
from flask import render_template

class RecordingGraph(DashboardElement):
    class RecordingGraphNamespace(Namespace):
        def on_connect(self):
            print(f"New client connected to GraphNamespace {self.element.namespace}")
            h_axis_data = self.element.recording.times
            v_axis_data = self.element.recording.samples
            self.element.update(h_axis_data, v_axis_data)

        def __init__(self, namespace, element):
            super().__init__(namespace)
            self.element = element


    def __init__(self, uid: str, recording: 'Recording', socketio: SocketIO = None):
        super().__init__(uid, socketio)
        self.recording = recording
        self._rolling = self.recording._rolling
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
            "uid": self.uid
        }
        return render_template("elements/recording_graph.js", data=data)
    
    def append_point(self, h_axis_datapoint, v_axis_datapoint):
        self.socketio.emit("append_point", {"h_axis_datapoint": h_axis_datapoint, "v_axis_datapoint": v_axis_datapoint}, namespace=self.namespace)

    def update(self, h_axis_data, v_axis_data):
        self.socketio.emit("update", {"h_axis_data": h_axis_data, "v_axis_data": v_axis_data}, namespace=self.namespace)
