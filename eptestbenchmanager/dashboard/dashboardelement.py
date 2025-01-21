from abc import ABC, abstractmethod
from flask_socketio import SocketIO


class DashboardElement(ABC):
    """Abstract base class for dashboard elements.

    Attributes:
        uid (str): Unique identifier for the dashboard element.
        socketio (SocketIO): Optional SocketIO instance for real-time communication.
    """

    def __init__(self, uid: str, socketio: SocketIO = None):
        """Initializes the DashboardElement with a unique identifier and optional SocketIO instance.

        Args:
            uid (str): Unique identifier for the dashboard element.
            socketio (SocketIO, optional): SocketIO instance for real-time communication.
            Defaults to None.
        """
        self.uid = uid
        self.socketio = socketio

    @abstractmethod
    def render_html(self):
        """Renders the HTML for the dashboard element.

        Returns:
            NotImplementedError: Indicates that the method should be implemented by subclasses.
        """
        return NotImplementedError("Implement render method")

    @abstractmethod
    def render_js(self):
        """Renders the JavaScript for the dashboard element.

        Returns:
            NotImplementedError: Indicates that the method should be implemented by subclasses.
        """
        return NotImplementedError("Implement render method")
