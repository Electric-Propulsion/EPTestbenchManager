from io import StringIO
from yaml import load, FullLoader
from .experiment import Experiment
from .experiment_segments import ExperimentSegment, Pumpdown, MeasureLeaks


class ExperimentFactory:

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")

    @classmethod
    def create_experiment(cls, config_file: StringIO, testbench_manager: 'TestbenchManager') -> Experiment:
        config = load(config_file, Loader=FullLoader)

        uid = config["experiment"]["uid"]
        name = config["experiment"]["name"]
        description = config["experiment"]["description"]

        segments = []

        for segment_type, segment_config in config["segments"].items():
            segment_uid = f"{uid}__{segment_type}"
            segment = cls.get_class(segment_type)(segment_uid, segment_config, testbench_manager)
            segments.append(segment)

        return Experiment(uid, name, description, segments)

    @classmethod
    def get_class(cls, segment_type) -> type:
        match segment_type:
            case "pumpdown":
                return Pumpdown
            case "measure_leaks":
                return MeasureLeaks
            case _:
                raise ValueError(f"Unknown segment type: {segment_type}")
