from flask import render_template
from flask_socketio import emit, Namespace

from ..dashboardelement import DashboardElement

class ExperimentControl(DashboardElement):
    def __init__(self, uid: str, testbench_manager: "TestbenchManager", socketio = None):
        super().__init__(uid, socketio)
        self.name = "Experiment Control"
        self.experiment_runner = testbench_manager.runner
        self.experiments = self.experiment_runner.experiments
        self.operators = testbench_manager.communication_engine.users #TODO: This is not great

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))
        self.configure() # set up the socketio events

    def render_html(self):
        data = {
            "experiments": self.experiments,
            "operators": self.operators,
            "uid": self.uid
        }
        print(data)
        value =  render_template("elements/experiment_control.html", data=data)
        print(value)
        return value
    
    def render_js(self):
        data = {
            "namespace": self.namespace,
            "uid": self.uid
        }
        return render_template("elements/experiment_control.js", data=data)
    
    def configure(self):
        @self.socketio.on('start_experiment', namespace=self.namespace)
        def start_experiment(data):
            print(f"experiment starting with {data}")
            self.experiment_runner.run_experiment(data['experiment_uid'], data['operator']) 

        @self.socketio.on('stop_experiment', namespace=self.namespace)
        def stop_experiment(data):
            print(f"experiment stopping")
