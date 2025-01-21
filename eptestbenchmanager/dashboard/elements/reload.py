from flask_socketio import Namespace, SocketIO
from flask import render_template
from ..dashboardelement import DashboardElement


class Reload(DashboardElement):
    """A class used to represent the Reload element in the dashboard.

    Attributes:
        uid (str): The unique identifier for the Reload element.
        socketio (SocketIO): The SocketIO instance for real-time communication.
        namespace (str): The namespace for the SocketIO instance.
    """

    def __init__(self, uid: str, socketio: SocketIO = None):
        """
        Initializes the Reload element with a unique identifier and an optional SocketIO instance.

        Args:
            uid (str): The unique identifier for the Reload element.
            socketio (SocketIO, optional): The SocketIO instance for real-time communication.
        """
        super().__init__(uid, socketio)
        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))

    def render_html(self) -> str:
        """
        Renders the HTML for the Reload element.

        Returns:
            str: An empty string as the Reload element does not require HTML.
        """
        return ""

    def render_js(self) -> str:
        """
        Renders the JavaScript for the Reload element.

        Returns:
            str: The rendered JavaScript template for the Reload element.
        """
        data = {"namespace": self.namespace, "uid": self.uid}
        return render_template("elements/reload.js", data=data)

    def reload(self):
        """
        Emits a reload event to the SocketIO namespace.
        """
        self.socketio.emit("reload", namespace=self.namespace)
