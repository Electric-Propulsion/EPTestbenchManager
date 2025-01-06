from flask import render_template
from flask_socketio import emit, Namespace

from ..dashboardelement import DashboardElement


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
            "operators": self.operators,
            "uid": self.uid,
        }
        value = render_template("elements/experiment_control.html", data=data)
        return value

    def render_js(self):
        """Renders the JavaScript for the experiment control dashboard element.

        Returns:
            str: Rendered JavaScript content.
        """
        data = {"namespace": self.namespace, "uid": self.uid}
        return render_template("elements/experiment_control.js", data=data)

    def configure(self):
        """Configures the socketio events for starting and stopping experiments."""

        @self.socketio.on("start_experiment", namespace=self.namespace)
        def start_experiment(data):
            """Handles the start_experiment event.

            Args:
                data (dict): Data containing experiment_uid and operator.
            """
            print(f"experiment starting with {data}")
            try:
                self.experiment_runner.run_experiment(
                    data["experiment_uid"], data["operator"]
                )
            except Exception as e:
                print(f"Error starting experiment: {e}")

        @self.socketio.on("stop_experiment", namespace=self.namespace)
        def stop_experiment(data):
            """Handles the stop_experiment event.

            Args:
                data (dict): Data containing experiment_uid and operator.
            """
            print(f"experiment stopping")
