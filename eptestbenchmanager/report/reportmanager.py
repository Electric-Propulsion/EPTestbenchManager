import logging
from pathlib import Path
import os
import zipfile
from typing import TYPE_CHECKING
from eptestbenchmanager.dashboard.elements import ArchiveDownload

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager

logger = logging.getLogger(__name__)


class ReportManager:
    """Manages reports (#TODO) and archives and log directories for the TestbenchManager.

    Attributes:
        testbench_manager (TestbenchManager): Global TestbenchManager object.
        _archive_dir (str): Directory path for storing archives.
        _log_dir (str): Directory path for storing logs.
        archives (list): List of archive names.
        ui_element (ArchiveDownload): UI element for archive download.
    """

    def __init__(
        self,
        testbench_manager: "TestbenchManager",
        archive_dir: str = None,
        log_dir: str = None,
    ):
        """Initializes ReportManager with given directories and testbench manager.

        Args:
            testbench_manager (TestbenchManager): Global TestbenchManager object.
            archive_dir (str, optional): Directory path for storing archives. Defaults to None.
            log_dir (str, optional): Directory path for storing logs. Defaults to None.
        """
        self.testbench_manager = testbench_manager
        self._archive_dir = None
        self._log_dir = None
        self.set_log_dir(log_dir)
        self.archives = []
        self.set_archive_dir(archive_dir)
        self.ui_element = self.testbench_manager.dashboard.create_element(
            ArchiveDownload, ("archive_download", self.testbench_manager, self)
        )

    def set_archive_dir(self, archive_dir):
        """Sets the archive directory and updates the list of archives.

        Args:
            archive_dir (str): Directory path for storing archives.
        """
        if archive_dir is None:
            archive_dir = os.path.join(
                Path(os.path.abspath(__package__)).parent,
                "eptestbenchmanager",
                "logs",
                "archives",
            )
        self._archive_dir = archive_dir
        try:
            self.archives = [
                Path(archive).stem for archive in os.listdir(self.archive_dir)
            ]
        except FileNotFoundError:
            self.archives = []

    def set_log_dir(self, log_dir):
        """Sets the log directory.

        Args:
            log_dir (str): Directory path for storing logs.
        """
        if log_dir is None:
            log_dir = os.path.join(
                Path(os.path.abspath(__package__)).parent, "eptestbenchmanager", "logs"
            )
        self._log_dir = log_dir

    @property
    def archive_dir(self):
        """Gets the archive directory.

        Returns:
            str: Directory path for storing archives.
        """
        return self._archive_dir

    @property
    def log_dir(self):
        """Gets the log directory.

        Returns:
            str: Directory path for storing logs.
        """
        return self._log_dir

    def create_archive(self, run_id, output_name_root) -> str:
        """Creates a zip archive of the log directory for a specific run.

        Args:
            run_id (str): Identifier for the run.
            output_name_root (str): Root name for the output archive file.

        Returns:
            str: Path to the created archive file.
        """
        run_log_dir = os.path.join(self.log_dir, run_id)
        output_archive_path = os.path.join(self.archive_dir, f"{output_name_root}.zip")
        os.makedirs(os.path.dirname(output_archive_path), exist_ok=True)
        logger.debug("Compressing log file directory: %s", run_log_dir)

        with zipfile.ZipFile(output_archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(run_log_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, run_log_dir)
                    zipf.write(file_path, arcname)
        logger.info("Directory %s compressed into %s", run_log_dir, output_archive_path)
        self.archives.append(output_name_root)

        self.ui_element.update_archives()

        return output_archive_path
