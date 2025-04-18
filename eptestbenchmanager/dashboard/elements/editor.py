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
        config_dir_name: str,
        config_name: str,
        socketio=None,
    ):
        self.testbench_manager = testbench_manager

        self.config_name = config_name
        self.config_dir_name = config_dir_name

        super().__init__(uid, socketio)

        # check if the file exists. If so, read it
        self.content = ""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.content = file.read()

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))
        self.configure()

    @property
    def file_path(self):
        """Returns the file path of the configuration."""
        try:
            file_path = self.testbench_manager.runtime_manager.configs[
                self.config_dir_name
            ][self.config_name].path
        except KeyError:
            # This is a new config, so we need to create it
            file_path = os.path.join(
                self.testbench_manager.runtime_manager.configs[
                    self.config_dir_name
                ].config_dir,
                self.config_name + ".yaml",
            )
            Path(file_path).touch(exist_ok=True)

        return file_path

    def save(
        self,
        content,
    ):
        logger.info("Saving file %s with content %s", self.file_path, content)
        with open(self.file_path, "w") as file:
            file.write(content)

        # need to somehow trigger the rest of the page to know that there's new apparatus configs
        self.testbench_manager.runner.load_experiments()
        self.testbench_manager.runtime_manager.configs[
            "apparatus_config"
        ].load_configs()

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
                "file_root": self.config_name,
            },
        )

    def render_js(self):
        return render_template(
            "elements/editor.js", data={"uid": self.uid, "namespace": self.namespace}
        )

    def configure(self):
        @self.socketio.on("save", namespace=self.namespace)
        def on_save(data):
            logger.info(f"Saving file with data {data}")
            old_config_name = self.config_name
            old_file_path = self.file_path
            self.config_name = data["file_root"]

            self.save(data["content"])

            renamed = old_config_name != self.config_name

            if renamed:
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                self.socketio.emit(
                    "save_status",
                    {"status": "success", "redirect": self.config_name},
                    namespace=self.namespace,
                )
            else:
                self.socketio.emit(
                    "save_status", {"status": "success"}, namespace=self.namespace
                )
