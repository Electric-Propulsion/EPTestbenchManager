from typing import TYPE_CHECKING
from flask import render_template
from flask_socketio import Namespace
import logging
from ..dashboardelement import DashboardElement

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager
    from eptestbenchmanager.connections import ConnectionManager

logger = logging.getLogger(__name__)


class ApparatusControl(DashboardElement):
    """Class to control and manage apparatus via a web dashboard."""

    def __init__(
        self,
        uid: str,
        connection_manager: "ConnectionManager",
        socketio=None,
    ):
        """Initializes the ApparatusControl instance.

        Args:
            uid (str): Unique identifier for the apparatus control instance.
            testbench_manager (TestbenchManager): Global TestbenchManager object.
            socketio (SocketIO, optional): SocketIO instance for real-time communication.
        """
        super().__init__(uid, socketio)
        self.name = "Apparatus Control"

        self.connection_manager = connection_manager
        self.apparatuses = self.connection_manager.apparatus_configs

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))
        self.configure()

    def render_html(self):
        """Renders the HTML for the apparatus control dashboard element.

        Returns:
            str: Rendered HTML content.
        """
        value = render_template(
            "elements/apparatus_control.html",
            data={"uid": self.uid, "apparatuses": self.apparatuses},
        )
        return value

    def render_js(self):
        """Renders the JavaScript for the apparatus control dashboard element."""

        value = render_template(
            "elements/apparatus_control.js",
            data={
                "namespace": self.namespace,
                "uid": self.uid,
                "apparatus_config_path": "apparatus_config",
            },
        )
        return value

    def configure(self):
        """Configures the socketio events for the apparatus control dashboard element."""

        @self.socketio.on("set_apparatus", namespace=self.namespace)
        def set_apparatus(data):
            logger.debug(f"Setting apparatus with {data}")
            try:
                self.connection_manager.set_apparatus_config(data["apparatus"])

            except Exception as e:
                logger.error(f"Error setting apparatus: {e}")
                logger.exception(e)
