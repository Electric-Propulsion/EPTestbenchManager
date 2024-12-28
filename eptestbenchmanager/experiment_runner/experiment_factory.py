from io import StringIO
from yaml import load, FullLoader
from threading import Lock
from .experiment import Experiment
from .experiment_segments import ExperimentSegment, Pumpdown, MeasureLeaks, Wait


class ExperimentFactory:

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")

    @classmethod
    def create_experiment(
        cls,
        config_file: StringIO,
        testbench_manager: "TestbenchManager",
        experiment_lock: Lock,
    ) -> Experiment:
        config = load(config_file, Loader=FullLoader)

        uid = config["experiment"]["uid"]
        name = config["experiment"]["name"]
        description = config["experiment"]["description"]

        segments = []

        for segment_uid, segment_config in config["segments"].items():
            segment_type = segment_config['type']
            segment_name = segment_config["name"]
            segment = cls.get_class(segment_type)(
                segment_uid, segment_name, segment_config, testbench_manager
            )
            segments.append(segment)


        experiment = Experiment(
            uid, name, description, segments, experiment_lock, testbench_manager
        )

        

        return experiment

    @classmethod
    def get_class(cls, segment_type) -> type:
        # TODO: make this so you can add new segment types without changing this code
        match segment_type:
            case "pumpdown":
                return Pumpdown
            case "measure_leaks":
                return MeasureLeaks
            case "wait":
                return Wait
            case _:
                raise ValueError(f"Unknown segment type: {segment_type}")
