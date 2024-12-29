from flask import Flask, render_template
from flask_socketio import SocketIO, emit, Namespace
from threading import Thread

class DashboardManager:
     def __init__(self, testbench_manager: "TestbenchManager"):
          self.testbench_manager = testbench_manager
          self.app = Flask(__name__)
          self.socketio = SocketIO(self.app)
          self.app.config["SECRET_KEY"] = 'testkey!' #TODO: change me!



     def run(self):

