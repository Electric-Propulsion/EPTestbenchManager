import logging
from typing import TYPE_CHECKING
from flask import render_template
from flask_socketio import Namespace
from ..dashboardelement import DashboardElement

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager

logger = logging.getLogger(__name__)


class ExperimentControl(DashboardElement):
    """Class to control and manage experiments via a web dashboard.

    Attributes:
        uid (str): Unique identifier for the experiment control instance.
        name (str): Name of the dashboard element.
        experiment_runner (ExperimentRunner): Runner to execute experiments.
        experiments (list): List of available experiments.
        operators (list): List of operators from the communication engine.
        namespace (str): Namespace for socketio communication.
        socketio (SocketIO): SocketIO instance for real-time communication.
    """

    def __init__(self, uid: str, testbench_manager: "TestbenchManager", socketio=None):
        """Initializes the ExperimentControl instance.

        Args:
            uid (str): Unique identifier for the experiment control instance.
            testbench_manager (TestbenchManager): Global TestbenchManager object.
            socketio (SocketIO, optional): SocketIO instance for real-time communication.
        """
        super().__init__(uid, socketio)
        self.name = "Experiment Control"
        self.estop = testbench_manager.estop
        self.experiment_runner = testbench_manager.runner
        self.experiments = self.experiment_runner.experiments
        self.operators = (
            testbench_manager.communication_engine.users
        )  # TODO: This is not great

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))
        self.configure()  # set up the socketio events

    def render_html(self):
        """Renders the HTML for the experiment control dashboard element.

        Returns:
            str: Rendered HTML content.
        """
        data = {
            "experiments": self.experiments,
            "operators": self.operators if self.operators is not None else [],
            "uid": self.uid,
        }
        value = render_template("elements/experiment_control.html", data=data)
        return value

    def render_js(self):
        """Renders the JavaScript for the experiment control dashboard element.

        Returns:
            str: Rendered JavaScript content.
        """
        data = {
            "namespace": self.namespace,
            "uid": self.uid,
            "experiment_config_path": "experiment_config",
        }
        return render_template("elements/experiment_control.js", data=data)

    def configure(self):
        """Configures the socketio events for starting and stopping experiments."""

        @self.socketio.on("start_experiment", namespace=self.namespace)
        def start_experiment(data):
            """Handles the start_experiment event.

            Args:
                data (dict): Data containing experiment_uid and operator.
            """
            logger.info("experiment starting with %s", data)
            try:
                self.experiment_runner.run_experiment(
                    data["experiment_uid"], data["operator"]
                )
            except Exception as e:
                logger.warning("Error starting experiment: %s", e)

        @self.socketio.on("request_abort", namespace=self.namespace)
        def request_abort():
            """Handles the stop_experiment event.

            Args:
                data (dict): Data containing experiment_uid and operator.
            """
            self.experiment_runner.request_abort_current_experiment()
            logger.info("Requesting abort of current experiment")

        @self.socketio.on("estop", namespace=self.namespace)
        def estop():
            """Handles the estop event."""
            self.estop.estop_fire()
