from typing import TYPE_CHECKING
from flask_socketio import Namespace, SocketIO
from flask import render_template
from ..dashboardelement import DashboardElement

if TYPE_CHECKING:
    from eptestbenchmanager.manager import Recording


class RecordingGraph(DashboardElement):
    """A class to represent a recording graph element in the dashboard.

    Attributes:
        uid (str): Unique identifier for the graph.
        recording (Recording): The recording object associated with the graph.
        socketio (SocketIO): The SocketIO instance for real-time communication.
        _rolling (bool): Indicates if the graph is rolling.
        _max_points (int): Maximum points to store if the graph is rolling.
        namespace (str): Namespace for the SocketIO communication.
    """

    class RecordingGraphNamespace(Namespace):
        """Namespace for handling SocketIO events for the recording graph.

        Methods:
            on_connect(): Handles new client connections.
        """

        def on_connect(self):
            """Handles new client connections.

            Emits an update event when a new client connects, so the client gets the full graph history.
            """
            print(f"New client connected to GraphNamespace {self.element.namespace}")
            self.element.update()

        def __init__(self, namespace, element):
            """Initializes the RecordingGraphNamespace with a namespace and element.

            Args:
                namespace (str): The namespace for the SocketIO communication.
                element (RecordingGraph): The recording graph element.
            """
            super().__init__(namespace)
            self.element = element

    def __init__(self, uid: str, recording: "Recording", socketio: SocketIO = None):
        """Initializes the RecordingGraph with a unique identifier, recording, and SocketIO instance.

        Args:
            uid (str): Unique identifier for the graph.
            recording (Recording): The recording object associated with the graph.
            socketio (SocketIO, optional): The SocketIO instance for real-time communication.
        """
        super().__init__(uid, socketio)
        self.recording = recording
        self._rolling = self.recording._rolling
        self._max_points = self.recording._stored_samples if self._rolling else 0
        self.namespace = f"/{uid}"
        self.socketio.on_namespace(self.RecordingGraphNamespace(self.namespace, self))

    def render_html(self):
        """Renders the HTML for the recording graph.

        Returns:
            str: Rendered HTML template for the recording graph.
        """
        data = {"uid": self.uid}
        return render_template("elements/recording_graph.html", data=data)

    def render_js(self):
        """Renders the JavaScript for the recording graph.

        Returns:
            str: Rendered JavaScript template for the recording graph.
        """
        data = {
            "namespace": self.namespace,
            "uid": self.uid,
            "rolling": self._rolling,
            "max_points": self._max_points,
            "name": self.recording.name,
            "measurement_name": self.recording.virtual_instrument.name,
            "measurement_unit": self.recording.virtual_instrument.unit,
            "t0": (
                self.recording._t0
                if self.recording._t0 is not None
                else self.recording._times[0]
            ),
        }
        return render_template("elements/recording_graph.js", data=data)

    def append_point(self, h_axis_datapoint, v_axis_datapoint, label):
        """Appends a new data point to the graph.

        Args:
            h_axis_datapoint (float): The horizontal axis data point.
            v_axis_datapoint (float): The vertical axis data point.
            label (str): The label for the data point.
        """
        self.socketio.emit(
            "append_point",
            {
                "h_axis_datapoint": h_axis_datapoint,
                "v_axis_datapoint": v_axis_datapoint,
            },
            namespace=self.namespace,
        )

    def update(self):
        """Updates the graph with the latest data from the recording.

        Emits an update event with the latest horizontal and vertical axis data.
        """
        h_axis_data = self.recording.times
        v_axis_data = self.recording.samples
        self.socketio.emit(
            "update",
            {"h_axis_data": h_axis_data, "v_axis_data": v_axis_data},
            namespace=self.namespace,
        )
