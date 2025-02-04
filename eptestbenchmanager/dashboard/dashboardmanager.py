import os
import logging
from pathlib import Path
from typing import TYPE_CHECKING
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

from .pages import MainPage
from .elements import ExperimentControl

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager
    from eptestbenchmanager.dashboard import DashboardElement, DashboardPage

logger = logging.getLogger(__name__)

class DashboardManager:
    """Manages the dashboard for the EP Testbench Manager.

    Attributes:
        testbench_manager (TestbenchManager): Global TestbenchManager object.
        app (Flask): The Flask application instance.
        socketio (SocketIO): The SocketIO instance for real-time communication.
        experiment_control (ExperimentControl): The experiment control element.
    """

    def __init__(self, testbench_manager: "TestbenchManager"):
        """Initializes the DashboardManager with the given testbench manager.

        Args:
            testbench_manager (TestbenchManager): The testbench manager instance.
        """
        self.testbench_manager = testbench_manager
        self.app = Flask(
            "eptestbenchmanager",
            static_folder="dashboard/assets/static",
            template_folder="dashboard/assets/templates",
        )
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.app.config["SECRET_KEY"] = "testkey!"  # TODO: change me!

    def configure(self):
        """Configures the routes and elements for the dashboard."""

        @self.app.route("/")
        def index():
            """Renders the main page."""
            page = self.create_page(MainPage, [self.testbench_manager])
            return page.render()

        vints = self.testbench_manager.connection_manager.virtual_instruments.values()
        for vint in vints:

            def make_instrument_detail(vint):
                @self.app.route(
                    f"/instrument/{vint.uid}", endpoint=f"instrument_detail_{vint.uid}"
                )
                def instrument_detail():
                    """Renders the instrument detail page."""
                    return vint.detail_page.render()

            make_instrument_detail(vint)

        # Special routes for downloading files
        @self.app.route("/archive/<archive>")
        def download_archive(archive):
            """Handles downloading of archive files."""
            archive_dir = os.path.join(
                Path(os.path.abspath(__package__)).parent,
                "eptestbenchmanager",
                "logs",
                "archives",
            )
            logger.info("Downloading archive %s", archive)
            try:
                return send_from_directory(archive_dir, f"{archive}")
            except Exception as e:
                logger.error("Error downloading archive: %s", e)

        # set up the experiment control elements
        # This must be done in the configure method so that the experiment runner is able to load
        # experiments before the experiment control element is created, but the dashboard manager
        # must be created first.
        self.experiment_control = (  # pylint: disable=attribute-defined-outside-init
            self.create_element(
                ExperimentControl, args=["experiment_control", self.testbench_manager]
            )
        )

    def create_element(self, element_class: "DashboardElement", args):
        """Creates a dashboard element.

        Args:
            element_class (DashboardElement): The class of the element to create.
            args (list): The arguments to pass to the element constructor.

        Returns:
            DashboardElement: The created element.
        """
        element_object = element_class(*args, **{"socketio": self.socketio})
        return element_object

    def create_page(self, page_class: "DashboardPage", args):
        """Creates a dashboard page.

        Args:
            page_class (DashboardPage): The class of the page to create.
            args (list): The arguments to pass to the page constructor.

        Returns:
            DashboardPage: The created page.
        """
        page_object = page_class(*args, **{"socketio": self.socketio, "app": self.app})
        return page_object

    def run(self):
        """Runs the dashboard, blocking the main thread."""
        logger.info("Starting dashboard - this will block the main thread")
        self.socketio.run(self.app, host="0.0.0.0")
