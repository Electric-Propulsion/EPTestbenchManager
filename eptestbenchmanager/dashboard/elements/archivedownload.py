from flask import render_template, send_from_directory
from flask_socketio import emit, Namespace
import os
from pathlib import Path

from ..dashboardelement import DashboardElement

class ArchiveDownload(DashboardElement):
    def __init__(self, uid: str, testbench_manager: "TestbenchManager", report_manager = 'ReportManager', socketio = None):
        super().__init__(uid, socketio)
        self.name = "Archive Download"
        self._report_manager = report_manager
        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))

    def render_html(self):
        data = {
            "archives": self._report_manager.archives,
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
    
    def update_archives(self):
        self.socketio.emit("update", {"archives": self._report_manager.archives}, namespace=self.namespace)