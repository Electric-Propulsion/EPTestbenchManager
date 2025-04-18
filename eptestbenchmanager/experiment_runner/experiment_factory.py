from io import StringIO
from threading import Lock
from typing import TYPE_CHECKING
from collections.abc import Iterable
from yaml import load, FullLoader
from .experiment import Experiment
from .experiment_segments import (
    Pumpdown,
    MeasureLeaks,
    Wait,
    IsoFilamentHold,
    IsoFilamentVoltageStep,
    Step, Hold, Set
)

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager


class ExperimentFactory:
    """Factory class for creating Experiment instances.

    This class is not meant to be instantiated. It provides class methods to create Experiment
    instances from configuration files.
    """

    def __init__(self):
        """Raises NotImplementedError to prevent instantiation."""
        raise NotImplementedError("This class is not meant to be instantiated")

    @classmethod
    def create_experiment(
        cls,
        config_file: StringIO,
        testbench_manager: "TestbenchManager",
        experiment_lock: Lock,
    ) -> Experiment:
        """Creates an Experiment instance from a configuration file.

        Args:
            config_file (StringIO): The configuration file for the experiment.
            testbench_manager (TestbenchManager): The manager for the testbench.
            experiment_lock (Lock): A lock for synchronizing experiment execution.

        Returns:
            Experiment: The created Experiment instance.
        """
        config = load(config_file, Loader=FullLoader)

        uid = config["experiment"]["uid"]
        name = config["experiment"]["name"]
        description = config["experiment"]["description"]
        experiment_recordings = config.get("recordings", None)

        segments = []

        for segment_uid, segment_config in config["segments"].items():
            segment_type = segment_config["type"]
            segment_name = segment_config["name"]
            if experiment_recordings is not None:
                segment_config["recordings"] = segment_config.get("recordings", []) + experiment_recordings
            # 'segment' could be a single segment or a list of segments
            segment = cls.get_class(segment_type)(
                segment_uid, segment_name, segment_config, testbench_manager
            )
            if isinstance(segment, Iterable):
                segments.extend(segment)
            else:
                segments.append(segment)

        experiment = Experiment(
            uid, name, description, segments, experiment_lock, testbench_manager
        )

        return experiment

    @classmethod
    def get_class(cls, segment_type) -> type:
        """Gets the class corresponding to the segment type.

        Args:
            segment_type (str): The type of the segment.

        Returns:
            type: The class corresponding to the segment type.

        Raises:
            ValueError: If the segment type is unknown.
        """
        match segment_type:
            case "pumpdown":
                return Pumpdown
            case "measure_leaks":
                return MeasureLeaks
            case "wait":
                return Wait
            case "iso_filament_hold":
                return IsoFilamentHold
            case "iso_filament_voltage_step":
                return IsoFilamentVoltageStep
            case "hold":
                return Hold
            case "step":
                return Step
            case "set":
                return Set
            case _:
                raise ValueError(f"Unknown segment type: {segment_type}")
