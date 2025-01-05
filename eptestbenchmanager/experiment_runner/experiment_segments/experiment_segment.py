from abc import ABC, abstractmethod
from threading import Thread
from os import path


from eptestbenchmanager.monitor import Rule

class AbortingSegmentFailure(Exception):
    # If this is raised, the experment should teminate
    pass


class ExperimentSegment(ABC):

    def __init__(self, uid: str, name: str, config: dict, testbench_manager: 'TestbenchManager'):
        self.uid = uid
        self.name = name
        self._rules: list[Rule] = []
        self._runner_thread: Thread = None
        self._testbench_manager = testbench_manager
        self.data = None
        self.configure(config)
        self._recordings = config["recordings"] if "recordings" in config else []
        self._segment_view = []
        self.experiment = None

    def inject_experiment(self, experiment):
        self.experiment = experiment

    @abstractmethod
    def configure(self, config: dict):
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError("Trying to run an abstract class!")

    @abstractmethod
    def generate_report(self):  # TODO: return type?
        raise NotImplementedError("Trying to generate a report from an abstract class.")

    @property
    def rules(self) -> list[Rule]:
        return self._rules
    
    def start_recordings(self):
        #breakpoint()
        for vinstrument_data in self._recordings:
            vinstrument_id = list(vinstrument_data.keys())[0]
            record_id = vinstrument_data[vinstrument_id]["record_id"]
            if vinstrument_id not in self._testbench_manager.connection_manager.virtual_instruments:
                raise ValueError(f"Virtual instrument {vinstrument_id} not found in testbench manager.")
            
            vinstrument = self._testbench_manager.connection_manager.virtual_instruments[vinstrument_id]
            
            if vinstrument.recording_exists(record_id):
                vinstrument.resume_recording(record_id)
            else:
                file_id = self.generate_file_ID(record_id)
                record_name = vinstrument_data[vinstrument_id]["record_name"]
                vinstrument.begin_recording(record_id, record_name, file_id=file_id)

    def stop_recordings(self):
        for vinstrument_data in self._recordings:
            vinstrument_id = list(vinstrument_data.keys())[0]
            record_id = vinstrument_data[vinstrument_id]["record_id"]
            if vinstrument_id not in self._testbench_manager.connection_manager.virtual_instruments:
                raise ValueError(f"Virtual instrument {vinstrument_id} not found in testbench manager.")
            
            vinstrument = self._testbench_manager.connection_manager.virtual_instruments[vinstrument_id]
            vinstrument.stop_recording(record_id)


    def prerun(self):
        self.start_recordings()

    def postrun(self):
        self.stop_recordings()

    def generate_file_ID(self, record_id: str):
        return path.join(self.experiment.run_id,record_id)
