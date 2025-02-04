import logging
from flask_socketio import emit, Namespace, SocketIO
from ..dashboardelement import DashboardElement

logger = logging.getLogger(__name__)


class CurrentValueElement(DashboardElement):
    """Represents a dashboard element that displays a current value.

    Attributes:
        name (str): The name of the element.
        value (any): The current value of the element.
        link (str): The url to the associated detail page.
        unit (str): The unit of the value.
        namespace (str): The namespace for the SocketIO communication.
        socketio (SocketIO): The SocketIO instance for real-time communication.
    """

    class CurrentValueNamespace(Namespace):
        """Namespace for handling SocketIO events for CurrentValueElement.

        Attributes:
            element (CurrentValueElement): The associated CurrentValueElement instance.
        """

        def on_connect(self):
            """Handles client connection to the namespace.

            Emits the current value and unit to the connected client.
            """
            logger.debug(f"Client connected to CurrentValueNamespace {self.element.namespace}")
            emit(
                "update",
                {"value": self.element.value, "unit": self.element.unit},
                namespace=self.element.namespace,
            )

        def __init__(self, namespace, element):
            """Initializes the CurrentValueNamespace.

            Args:
                namespace (str): The namespace for the SocketIO communication.
                element (CurrentValueElement): The associated CurrentValueElement instance.
            """
            super().__init__(namespace)
            self.element = element

    def __init__(
        self,
        uid: str,
        name: str,
        linked_instrument_uid: str = None,
        unit: str = None,
        socketio: SocketIO = None,
    ):
        """Initializes the CurrentValueElement.

        Args:
            uid (str): The unique identifier for the element.
            name (str): The name of the element.
            linked_instrument_uid (str, optional): The UID of the linked instrument.
            unit (str, optional): The unit of the value.
            socketio (SocketIO, optional): The SocketIO instance for real-time communication.
        """
        super().__init__(uid, socketio)
        self.name = name
        self.value = None
        self.link = (
            f"/instrument/{linked_instrument_uid}" if linked_instrument_uid else None
        )
        self.unit = unit

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(self.CurrentValueNamespace(self.namespace, self))

    def set_value(self, value):
        """Sets the current value and emits an update event.

        Args:
            value (any): The new value to set.
        """
        self.value = value

        # Derived classes must have client-side JS that listens for the 'update' event
        self.socketio.emit(
            "update", {"value": self.value, "unit": self.unit}, namespace=self.namespace
        )
