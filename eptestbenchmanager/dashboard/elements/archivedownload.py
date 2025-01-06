from typing import TYPE_CHECKING
from flask import render_template
from flask_socketio import Namespace

from ..dashboardelement import DashboardElement

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager
    from eptestbenchmanager.report import ReportManager


class ArchiveDownload(DashboardElement):
    """Class for handling archive downloads in the dashboard.

        Attributes:
            uid (str): Unique identifier for the element.
            testbench_manager (TestbenchManager):           # set up the experiment control elements
    .
            report_manager (ReportManager): Manager for reports.
            socketio (SocketIO): SocketIO instance for real-time communication.
            name (str): Name of the element.
            namespace (str): Namespace for SocketIO communication.
    """

    def __init__(
        self,
        uid: str,
        testbench_manager: "TestbenchManager",
        report_manager: "ReportManager" = None,
        socketio=None,
    ):
        """Initializes ArchiveDownload with the given parameters.

        Args:
            uid (str): Unique identifier for the element.
            testbench_manager (TestbenchManager): Global TestbenchManager object.
            report_manager (ReportManager, optional): Manager for reports. Defaults to None.
            socketio (SocketIO, optional): SocketIO instance for real-time communication.
            Defaults to None.
        """
        super().__init__(uid, socketio)
        self.name = "Archive Download"
        self._report_manager = report_manager
        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))
        self.testbench_manager = (
            testbench_manager  # TODO: evaluate if this is necessary
        )

    def render_html(self):
        """Renders the HTML for the archive download element.

        Returns:
            str: Rendered HTML content.
        """
        data = {"archives": self._report_manager.archives, "uid": self.uid}
        value = render_template("elements/archive_download.html", data=data)
        return value

    def render_js(self):
        """Renders the JavaScript for the archive download element.

        Returns:
            str: Rendered JavaScript content.
        """
        data = {"namespace": self.namespace, "uid": self.uid}
        return render_template("elements/archive_download.js", data=data)

    def update_archives(self):
        """Emits an update event with the current archives.

        Emits:
            update: Event with the current archives.
        """
        self.socketio.emit(
            "update",
            {"archives": self._report_manager.archives},
            namespace=self.namespace,
        )
