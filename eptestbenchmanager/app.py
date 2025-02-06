from eptestbenchmanager.manager import TestbenchManager
from flask import Flask

app = Flask(
    "eptestbenchmanager",
    static_folder="dashboard/assets/static",
    template_folder="dashboard/assets/templates",
)

app_root = TestbenchManager(app)
