from flask import render_template, send_from_directory
from flask_socketio import emit, Namespace
import os
from pathlib import Path

from ..dashboardelement import DashboardElement

class ArchiveDownload(DashboardElement):
    def __init__(self, uid: str, testbench_manager: "TestbenchManager", socketio = None):
        super().__init__(uid, socketio)
        self.name = "Archive Download"
        self.archive_dir = os.path.join(Path(os.path.abspath(__package__)).parent, "eptestbenchmanager", "logs", "archives") # what a terrific line of code.
        self.archives = [Path(archive).stem for archive in os.listdir(self.archive_dir)]
        print(self.archives)
        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))

    def render_html(self):
        data = {
            "archives": self.archives,
            "uid": self.uid
        }
        value =  render_template("elements/archive_download.html", data=data)
        return value
    
    def render_js(self):
        data = {
            "namespace": self.namespace,
            "uid": self.uid
        }
        return render_template("elements/archive_download.js", data=data)