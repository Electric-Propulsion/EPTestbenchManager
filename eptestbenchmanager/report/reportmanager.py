from pathlib import Path
import os
import zipfile

from eptestbenchmanager.dashboard.elements import ArchiveDownload

class ReportManager:
    def __init__(self, testbench_manager: "EPTestbenchManager", archive_dir: str = None, log_dir: str = None):
        self.testbench_manager = testbench_manager
        self._archive_dir = None
        self._log_dir = None
        self.set_log_dir(log_dir)
        self.archives = []
        self.set_archive_dir(archive_dir)
        self.ui_element = self.testbench_manager.dashboard.create_element(ArchiveDownload, ('archive_download', self.testbench_manager, self))
        
    def set_archive_dir(self, archive_dir):
        if archive_dir is None:
            archive_dir = os.path.join(Path(os.path.abspath(__package__)).parent, "eptestbenchmanager", "logs", "archives")
        self._archive_dir = archive_dir
        try:
            self.archives = [Path(archive).stem for archive in os.listdir(self.archive_dir)]
        except FileNotFoundError:
            self.archives = []

    def set_log_dir(self, log_dir):
        if log_dir is None:
            log_dir = os.path.join(Path(os.path.abspath(__package__)).parent, "eptestbenchmanager", "logs")
        self._log_dir = log_dir

    @property
    def archive_dir(self):
        return self._archive_dir
    
    @property
    def log_dir(self):
        return self._log_dir

    def create_archive(self, run_ID, output_name_root) -> str:
        run_log_dir = os.path.join(self.log_dir, run_ID)
        output_archive_path = os.path.join(self.archive_dir, f"{output_name_root}.zip")
        os.makedirs(os.path.dirname(output_archive_path), exist_ok=True)
        print(f" Compressing log file directory: {run_log_dir}")

        with zipfile.ZipFile(output_archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(run_log_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(file_path)
                    # Add file to zip, preserving the directory structure
                    arcname = os.path.relpath(file_path, run_log_dir)
                    zipf.write(file_path, arcname)
        print(f"Directory {run_log_dir} compressed into {output_archive_path}")
        self.archives.append(output_name_root)

        self.ui_element.update_archives()

        return output_archive_path
    

