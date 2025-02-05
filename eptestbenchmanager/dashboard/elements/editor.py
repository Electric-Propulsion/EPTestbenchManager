from flask import render_template
from flask_socketio import Namespace
import os
from pathlib import Path
import logging

from .. import DashboardElement

logger = logging.getLogger(__name__)


class Editor(DashboardElement):
    def __init__(
        self,
        uid: str,
        testbench_manager: "TestbenchManager",
        edit_dir: Path,
        filename: str,
        socketio=None,
    ):
        self._edit_dir = edit_dir
        self.filename = filename
        self.testbench_manager = testbench_manager

        self._file_path = self.safe_join(self._edit_dir, self.filename)

        super().__init__(uid, socketio)

        # check if the file exists. If so, read it
        self.content = ""
        if os.path.exists(self._file_path):
            with open(self._file_path, "r") as file:
                self.content = file.read()

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))
        self.configure()

    def save(
        self,
        content,
    ):
        logger.info("Saving file %s with content %s", self._file_path, content)
        with open(self._file_path, "w") as file:
            file.write(content)

        # need to somehow trigger the rest of the page to know that there's new apparatus configs
        self.testbench_manager.runner.load_experiments()
        self.testbench_manager.connection_manager.update_apparatus_configs()

    def safe_join(self, base, *paths):
        """Safely joins a path with a base path."""

        final_path = os.path.abspath(os.path.join(base, *paths))
        if not final_path.startswith(str(base)):
            logger.error("Path is outside of the base path - youre gonna get hacked")
        return final_path

    def render_html(self):
        return render_template(
            "elements/editor.html",
            data={
                "uid": self.uid,
                "content": self.content,
                "file_root": self.filename.split(".")[0],
            },
        )

    def render_js(self):
        return render_template(
            "elements/editor.js", data={"uid": self.uid, "namespace": self.namespace}
        )

    def configure(self):
        @self.socketio.on("save", namespace=self.namespace)
        def on_save(data):
            logger.debug(f"Saving file with data {data}")
            old_filename = self.filename
            self.filename = f"{data["file_root"]}.yaml"

            self._file_path = self.safe_join(self._edit_dir, self.filename)

            self.save(data["content"])

            renamed = old_filename != self.filename

            if renamed:
                if os.path.exists(self.safe_join(self._edit_dir, old_filename)):
                    os.remove(self.safe_join(self._edit_dir, old_filename))
                self.socketio.emit(
                    "save_status",
                    {"status": "success", "redirect": self.filename},
                    namespace=self.namespace,
                )
            else:
                self.socketio.emit(
                    "save_status", {"status": "success"}, namespace=self.namespace
                )
